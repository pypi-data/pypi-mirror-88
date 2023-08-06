import plotly.io as pio
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode()
#pio.renderers.keys()
#pio.renderers.default = 'jupyterlab'

import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns

# Improve resolution of output graphcis
#%config InlineBackend.figure_format ='retina'

import pandas as pd
import numpy as np

#import dask.dataframe as dd
#from dask.distributed import Client
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import roc_auc_score,f1_score,confusion_matrix, plot_confusion_matrix, classification_report
#import xgboost as xgb
#import shap
#shap.initjs()
#from umap import UMAP
#import hdbscan
#from kedro.framework.context import load_context

# need to load in the params then run the init file 
#to make `reload_kedro` available
# from IPython.core.magic import register_line_magic
# context = load_context("../")

# @register_line_magic
# def reload_kedro_mod(line):
#     "my line magic"
#     %run {context.params['kedro_ipython_init_path']}
#     return line

#%reload_kedro_mod

def fix_chipseq_df_columns(chip_original_df:pd.DataFrame):
    fixed_cols = chip_original_df.columns.tolist()
    fixed_cols.remove("Unnamed: 4")
    correct_cols_df = chip_original_df.dropna(axis=1)
    correct_cols_df.columns = fixed_cols
    return correct_cols_df

def transpose_case_row_col_peak(df):
    sample_cols = df.loc[:,"C_34_ME":].columns
    peaks = df[["chr", "start", "end"]].astype("str").apply("_".join, axis=1).tolist()
    df_correct = df.loc[:,"C_34_ME":].T
    df_correct.columns = peaks
    return df_correct

def process_sample_covs(sample_covs):
    sample_covs_cleaned = sample_covs.copy()
    
    #**Change the sample ID to `C_24_DO` and the Diagnosis for that sample**
    sample_covs_cleaned['ChIP-Seq ID'] = sample_covs_cleaned['ChIP-Seq ID'].replace("O_24_DO", "C_24_DO")
    sample_covs_cleaned.loc[sample_covs_cleaned['ChIP-Seq ID'] == 'C_24_DO', "Diagnosis"] = "Control"
    return sample_covs_cleaned

#test = process_sample_covs(catalog.load("sample_covs"))

#assert test.equals(sample_covs)

def make_processed_datasets(sample_covs_raw, df_correct, important_covs):
    sample_covs = process_sample_covs(sample_covs_raw)
    
    #**Left join of `ChIP data` and `sample covariates`**
    
    merged = df_correct.merge(sample_covs, right_on="ChIP-Seq ID", left_index=True, how="left")
    merged = merged.reset_index()
    merged.index = df_correct.index
    merged.index.name = "ChIP-Seq ID"

    #**rename columns**

    merged = merged.rename(columns={"index": "sample_covs_index",
                                   'Race           USA Category': "Race USA Category",
                                   'Ethnicity                           USA Category': 'Ethnicity USA Category'})
    
    peak_columns = merged.columns[merged.columns.str.startswith("chr")].tolist()#[column for column in merged.columns if column.startswith("chr")]
    non_peak_columns = merged.columns.difference(peak_columns).tolist()


    merged = merged.drop(columns = ['ChIP Comments',
                                    'NOTES1',
                                    'NOTES2'])
    
    #fix PMI and ethnicity columns

    merged["PMI"]=merged["PMI"].replace({'~24':24, '50.0*': 50}).astype(float)
    merged["Ethnicity USA Category"] = merged["Ethnicity USA Category"].replace({'Non-Hspanic/ Latino': 'Non-Hispanic/ Latino',
                                                                                'HIspanic/Latino': 'Hispanic/Latino'})
    sample_covs_inherent_samples_only = merged[sample_covs.columns.difference(["ChIP-Seq ID"] + ['NOTES1', 'ChIP Comments', 'NOTES2', 'Race           USA Category', 'Ethnicity                           USA Category'])]

    #**Create `case_control_status` column and check with `Diagnosis` column**

    cc_status_diagnosis = np.where(sample_covs_inherent_samples_only.Diagnosis.str.strip() == "Control", 0, 1)
    cc_status_chip_id = np.where(merged.index.str.startswith("C"), 0, 1)

    assert np.equal(cc_status_diagnosis, cc_status_chip_id).all()
    
    merged["case_control_status"] = cc_status_chip_id
    
    important_covs_and_cc_status = merged[important_covs + ["case_control_status"]]
    important_covs_and_cc_status
    return sample_covs_inherent_samples_only, important_covs_and_cc_status


def make_ML_matrix(important_covs_and_cc_status, df_correct):
    assert important_covs_and_cc_status.shape[0] == df_correct.shape[0]
    ## don't understand why the following line was needed, for some reason important_covs_and_cc_status was not saved with index
    important_covs_and_cc_status.index = df_correct.index
    important_covs_and_cc_status_dummified = pd.get_dummies(important_covs_and_cc_status)
    ML_X_y_matrix = df_correct.join(important_covs_and_cc_status_dummified)
    
    return important_covs_and_cc_status_dummified, ML_X_y_matrix

#test, test1 = make_ML_matrix(important_covs_and_cc_status, df_correct)

#assert test.equals(important_covs_and_cc_status_dummified)
#assert test1.equals(ML_X_y_matrix)
