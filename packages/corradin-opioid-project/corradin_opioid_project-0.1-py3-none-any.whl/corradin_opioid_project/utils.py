import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score,f1_score,confusion_matrix, plot_confusion_matrix, classification_report
import xgboost as xgb
import shap
shap.initjs()
import matplotlib.pyplot as plt
from pickle import dump
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client
from scipy.stats import ttest_ind
from collections import defaultdict
from tqdm.auto import tqdm
import logging
from umap import UMAP
import hdbscan
from contextlib import nullcontext
from IPython.utils import io
from collections.abc import Iterable
from functools import wraps
from dataclasses import dataclass, field, make_dataclass, asdict
from typing import ClassVar
from functools import partial
from collections import UserDict
import pprint
from typing import Callable, Iterator, Union, Optional, List, Any
import seaborn as sns
from sklearn.metrics import silhouette_score

from fastcore.foundation import *
from fastcore.meta import *
from fastcore.utils import *
from fastcore.test import *
from nbdev.showdoc import *
from fastcore.dispatch import typedispatch
from functools import partial

#was trying to write custom __eq__ and custom __hash__ to override eq = True, which needs the two instances being compared to be of the exact same class
def dataclass_from_dict(name,input_dict):
#     def __eq__(self, other):
#         inst_fields = self.__dataclass_fields__.keys()
#         return all([self.__dict__[attr] == other.__dict__[attr] for attr in inst_fields])
#     def __hash__(self):
#         inst_fields = self.__dataclass_fields__.keys()
#         return hash(tuple([self.__dict__[attr] for attr in inst_fields])) 
    
    return make_dataclass(name, fields = [(k,type(v)) for k,v in input_dict.items()], frozen=True,) #eq=False, namespace={"__eq__": __eq__, "__hash__": __hash__})


#subclassing dict to extend dict functionalities
class DataClassDict(UserDict):
    """
    Accept dataclass as key with pretty repr string and ability to query the dictionary with dataclass instance key

    Args:
        UserDict ([type]): [description]
    """

    def __init__(self, data, cls:dataclass):
        """[summary]

        Args:
            data ([type]): inherited data from Python's UserDict
            cls (dataclass): the dataclass being used as keys
        """
        super(DataClassDict, self).__init__()
        self.data = data
        self._cls = cls
        self._keys =  super(DataClassDict, self).keys
        
    def __repr__(self):
        from pprint import pformat
        return pformat(str(list(self.keys()))).strip("()")
    
    def query(self, *args, **kwargs):
        """Construct a dataclass key using keyword arguments and return value of that key

        Returns:
            Value of the dataclass key stored in this dictionary
        """
        key_instance = self._cls(**kwargs) 
        return self.data[key_instance]

    def keys(self):
        return list(self._keys())#[k for k,v in self.data.items()]
    
    
    def to_pandas(self, attr: str) -> pd.core.frame.DataFrame:
        def to_pandas_single_df(dc_val, attr):
            col_name = ("|").join([f"func={dc_val.func_name}", *[("=").join([str(k), str(v)]) for k,v in dc_val.args.items()]])
            attr_val = dc_val.return_vals[attr]
            df = pd.DataFrame(attr_val, columns = [col_name] * attr_val.shape[1] if isinstance(attr_val, (np.ndarray, pd.core.frame.DataFrame)) else col_name)
            return df
        return pd.concat([to_pandas_single_df(dc_val, attr) for dc_val in self.values()], axis=1)

#     def to_pandas(self):
#         return pd.DataFrame

def repeated_call(parameters_dict):
    
    def wrapper(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs): 
            """A wrapper function"""
        
    return wrapper

def return_with_args(return_vals, filterable=False, return_args=None, pre_process=None,*args, **kwargs):
#     def _preprocess(ele: ):
#         if isinstance(ele, )
    
    import inspect
    def wrapper(func):
        @wraps(func)
        def _wrapped_func(*args, rename_dict=None, return_vals_filtered=[], **kwargs): 
            """A wrapper function"""
            # Extend some capabilities of func
            make_dataclass_mod = partial(make_dataclass, frozen=True, eq=True)
            func_locals_dict = func(*args, **kwargs)
            ##allow user to filter and rename variables
            return_vals_mod = return_vals_filtered if filterable else return_vals
            return_vals_mod = return_vals_mod if rename_dict is None else [rename_dict[val] for val in return_vals_mod]
            return_args_mod = inspect.getargspec(func).args if return_args is None else return_args 
            
            base_class_name = f"{func.__name__}_Result_Base"
            
            locals()[base_class_name]= make_dataclass_mod(base_class_name, [('args', dict), ('return_vals', dict)])
            created_class = locals()[base_class_name]
            
            #include the result class within the object
            
            wrapper_class_name = f"{func.__name__}_Result"
            locals()[wrapper_class_name] = make_dataclass_mod(wrapper_class_name, 
                                                                              fields=[('result_class', object), ("fields", list),("func_name", str)], bases=(created_class,))
            
            
            created_wrapper_class = locals()[wrapper_class_name]
            
            args_class_name = f"{func.__name__}_Args"
            
            return_dict = {
                           "args": {k:v for k,v in func_locals_dict.items() if k in return_args_mod},
                           "return_vals": {k:v for k,v in func_locals_dict.items() if k in return_vals_mod}
                          }
            
            created_wrapper_class.__repr__ = lambda self: f"<{created_wrapper_class.__name__} object, fields: {list(created_wrapper_class.__dataclass_fields__.keys())}>"
            return_result_instance = created_class(**return_dict)
            return_wrapper_instance = created_wrapper_class(**{"result_class": created_class, "fields" : list(created_class.__dataclass_fields__.keys()), "func_name": func.__name__}, **return_dict)
            return return_wrapper_instance
        return _wrapped_func
                       
    return wrapper

    

def predict_ensemble(ensemble, X):
    """
    predict_ensemble runs the X data set through
    each classifier in the ensemble list to get predicted
    probabilities.
    Those are then averaged out across all classifiers. 
    """
    probs = [r.predict_proba(X)[:,1] for r in ensemble]
    return np.vstack(probs).mean(axis=0)

def adjusted_classes(y_scores, t):
    """
    This function adjusts class predictions based on the prediction threshold (t).
    Will only work for binary classification problems.
    """
    return [1 if y >= t else 0 for y in y_scores]


def print_report(m, X_valid, y_valid, t=0.5, X_train=None, y_train=None, show_output=True):
    """
    print_report prints a comprehensive classification report
    on both validation and training set (if provided).
    The metrics returned are AUC, F1, Precision, Recall and 
    Confusion Matrix.
    It accepts both single classifiers and ensembles.
    Results are dependent on the probability threshold t 
    applied to individual predictions.
    """
#     X_train = X_train.values
#     X_valid = X_valid.values
    
    if isinstance(m, list):
        probs_valid = predict_ensemble(m, X_valid)
        y_val_pred = adjusted_classes(probs_valid, t)
    
        if X_train is not None:
            probs_train = predict_ensemble(m, X_train)
            y_train_pred = adjusted_classes(probs_train, t)
    else:
        probs_valid = m.predict_proba(X_valid)[:,1]
        y_val_pred = adjusted_classes(probs_valid, t)
        
        if X_train is not None:
            probs_train = m.predict_proba(X_train)[:,1]
            y_train_pred = adjusted_classes(probs_train, t)
    
    res = [roc_auc_score(y_valid, probs_valid),
           f1_score(y_valid, y_val_pred),
           confusion_matrix(y_valid, y_val_pred)]
    result = f'AUC valid: {res[0]} \nF1 valid: {res[1]}'
    
    if X_train is not None:
        res += [roc_auc_score(y_train, probs_train),
                f1_score(y_train, y_train_pred)]
        result += f'\nAUC train: {res[3]} \nF1 train: {res[4]}'
    
    acc_train = m.score(X_train, y_train)
    acc_valid = m.score(X_valid, y_valid)
    
    if show_output:
        logging.info(f"train acc: {acc_train}")
        logging.info(f"test acc: {acc_valid} ")

        logging.info(result)
        plot_confusion_matrix(m, X_valid, y_valid,
                                     display_labels= y_valid.unique())
        logging.info(classification_report(y_valid, y_val_pred))
        plt.show()
    return {"train":{"AUC": res[3], "F1": res[4], "acc": acc_train}, "test":{"AUC": res[0], "F1": res[1], "acc": acc_valid}}


def fit_classification(X: Union[pd.DataFrame, np.ndarray],
X_train: Union[pd.DataFrame, np.ndarray], 
X_test: Union[pd.DataFrame, np.ndarray], 
y_train: Union[pd.Series, np.ndarray], 
y_test: Union[pd.Series, np.ndarray], 
early_stopping: bool = True,  
name: str = "Unnamed model", 
fitted: bool =False,  
show_output: bool =True , 
model=None,
path= None, 
**kwargs):
    """[summary]

    Args:
        X (Union[pd.DataFrame, np.ndarray]): Full X for consistent feature importance calculation
        X_train (Union[pd.DataFrame, np.ndarray]): [description]
        X_test (Union[pd.DataFrame, np.ndarray]): [description]
        y_train (Union[pd.Series, np.ndarray]): [description]
        y_test (Union[pd.Series, np.ndarray]): [description]
        early_stopping (bool, optional): [description]. Defaults to True.
        name (str, optional): [description]. Defaults to "Unnamed model".
        fitted (bool, optional): [description]. Defaults to False.
        show_output (bool, optional): [description]. Defaults to True.
        model ([type], optional): [description]. Defaults to None.
        path ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    if not fitted:
        print(f"extra XGBoost kwargs: {kwargs}")
        if not model:
            model = xgb.XGBClassifier(verbosity = 0, random_state=42, **kwargs)#xgb.XGBClassifier(n_estimators=100,  subsample=0.8, colsample_bytree=0.5)
        eval_set = [(X_train, y_train), (X_test, y_test)]
        eval_metric = ["error", "logloss", "auc"]
        
        # check if multi-label classification
        if "num_class" in kwargs.keys():
            eval_metric += ["merror", "mlogloss"]
        print(X_train.shape, y_train.shape)
        print(eval_metric)
        
        if early_stopping:
            fitted = model.fit(X_train,y_train, early_stopping_rounds=5, eval_metric=eval_metric,  eval_set=eval_set)
            
        else:
            fitted = model.fit(X_train,y_train, eval_metric=["error", "logloss", "auc", "aucpr", "map"],  eval_set=eval_set)
            
        results = model.evals_result()

    metrics_dict = print_report(model, X_test, y_test, t=0.5, X_train=X_train, y_train=y_train, show_output=show_output)
    
    if path:
        dump(fitted, open(path, 'wb'))
    
    shap_values_non_zero, important_feat = get_shap_info(model, X, name)
    return {"shap_df": shap_values_non_zero, "important_feat":important_feat, "metrics":metrics_dict, "model":model, "train_index": X_train.index, "test_index": X_test.index}

@delegates(fit_classification)
def train_output_metrics( X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray] , test_size=0.3,  no_seed: bool = False, **kwargs):
    """[summary]

    Args:
        X (Union[pd.DataFrame, np.ndarray]): [description]
        y (Union[pd.Series, np.ndarray]): [description]
        test_size (float, optional): [description]. Defaults to 0.3.
        no_seed (bool, optional): Whether to set a seed for train/test splitting for reproducibility. Defaults to False.

    Returns:
        [type]: [description]
    """
    if no_seed:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
                                                        stratify=y)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,random_state=42, stratify=y)
    

    logging.info(f"train size:{1- test_size}, test_size:{test_size}")
    logging.info(f"train case/control num {y_train.value_counts()[1]}/{y_train.value_counts()[0]}")
    logging.info(f"test case/control num  {y_test.value_counts()[1]}/{y_test.value_counts()[0]}")
        
    return fit_classification(X, X_train, X_test, y_train, y_test, **kwargs)



def get_shap_info(model,X,name):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    shap_values_non_zero = pd.DataFrame(shap_values, columns = X.columns).loc[:, shap_values.sum(axis=0) != 0]
    important_feat = np.abs(shap_values_non_zero).mean().sort_values(ascending=False)
    
    formatted_name = name.format()
    important_feat.name = f"shap_vals"
    important_feat = important_feat.to_frame()
    important_feat["model_name"] = name
    return shap_values_non_zero, important_feat

# def train_multi_params(*args, param_dict:dict=None, func=None, **kwargs):
#     if None in [changing_param, func]:
#         raise ValueError
#     else:
#         results = defaultdict(dict)
#         for key in tqdm(param_dict):
#             for val in tqdm(param_dict[key]):
#                 new_dict = kwargs.copy()
#                 new_dict[key] = val
#                 results[key][val] = func(*args,**new_dict)

def repeat_train(X, y, num_times, different_train_test_split, name, model=None, silent=False, **kwargs):
    result_list =[]
    print(f"Extra params: {kwargs}")
    for i in tqdm(range(num_times)):
        with io.capture_output() if silent else nullcontext() as captured :
            result_dict = train_output_metrics(X, y, name="base_model",no_seed=different_train_test_split, early_stopping=True, model=model, **kwargs)
            result_list.append(result_dict)
    auc_list = [metric_dict["metrics"]["test"]["AUC"] for metric_dict in result_list]
    auc_df = pd.DataFrame({"AUC": auc_list, "dataset":name})
    fig = px.violin(auc_df, box=True, y = "AUC", color = "dataset")
    return {"AUC":auc_df, "result_list": result_list, "fig": fig}


def plot_curve(model_evals_result):
    results = model_evals_result
    epochs = len(results['validation_0']['error'])
    x_axis = range(0, epochs)
    # plot log loss
    train_df = pd.DataFrame.from_dict(base_model.evals_result()["validation_0"], orient="columns")
    train_df["set"] = "train"
    test_df = pd.DataFrame.from_dict(base_model.evals_result()["validation_1"], orient="columns")
    test_df["set"] = "test"
    combined = pd.concat([train_df, test_df])
    
    for column in combined.drop(columns="set").columns:
        fig = px.line(combined, x = combined.index, y=column, color ="set")
        fig.show()
#         fig, ax = plt.subplots()
#         ax.plot(x_axis, results['validation_0'][metric], label='Train')
#         ax.plot(x_axis, results['validation_1'][metric], label='Test')
#         ax.legend()
#         plt.ylabel(f'{metric}')
#         plt.title(f'XGBoost {metric}')
#         plt.show()

@return_with_args(return_vals=["multi_param_result_dict"])
def draw_umap(data,n_neighbors=None, min_dist=None, c=None,  n_components=None, metric='euclidean', title="Untitled_exp", plot=True, plotly_3D = True, return_vals_filtered=["u","mapper"], umap_kwargs={}, **kwargs):
    @return_with_args(return_vals=["u", "mapper"], filterable = True)
    def draw_one_umap(one_n_neighbor, one_min_dist, one_n_component):
        fit = UMAP(
        n_neighbors= one_n_neighbor,
        min_dist= one_min_dist,
        n_components=one_n_component,
        metric=metric,
        random_state = 42,
        **umap_kwargs
    )
        
        mapper = fit.fit(data);
        u = fit.transform(data);
        
        fig = None
        final_title = f"{title}: {one_n_component}D representation, n_neighbor: {one_n_neighbor}, min_dist: {one_min_dist}"
        
        if plot:
#             if one_n_component == 1:
#                 ax = fig.add_subplot(111)
#                 ax.scatter(u[:,0], range(len(u)), c=c)
            fig = plt.figure()
    
            if one_n_component == 2:
                ax = fig.add_subplot(111)
                scatter = ax.scatter(u[:,0], u[:,1], c=c, label=c)
                plt.title(final_title, fontsize=18)
                legend = ax.legend(*scatter.legend_elements())
                ax.add_artist(legend)
                plt.show()
            if one_n_component == 3:
                
#                 ax = fig.add_subplot(111, projection='3d')
#                 scatter = ax.scatter(u[:,0], u[:,1], u[:,2], c=c, s=100)
                
                if plotly_3D:
                    plotly_fig_3D = px.scatter_3d(x=u[:,0], y=u[:,1], z=u[:,2],color=c, opacity = 0.3, title = final_title, **kwargs)
                    plotly_fig_3D.update_layout(legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ))

                    display(plotly_fig_3D)
    

            
        u = pd.DataFrame(u, columns = [f"UMAP_{one_n_component}D_{i}" for i in range(1, one_n_component+1)], index=data.index)        
        return locals()
    
    standardize_input = lambda x, default: list(x) if isinstance(x, Iterable) else default if x is None else [x]
    
    n_neighbor_list = standardize_input(n_neighbors, [5,10, 20, 50, 100, 200])
    min_dist_list = standardize_input(min_dist, [0, 0.1])
    n_component_list = standardize_input(n_components, [2,3])
    
    multi_param_result_dict = {}
    
    MultiParamClass = None
    
    for one_min_dist in min_dist_list:
        for one_n_neighbor in n_neighbor_list:
            if one_n_neighbor >= data.shape[0]:
                continue
            for one_n_component in n_component_list:                       
                returned_instance = draw_one_umap(one_n_neighbor, one_min_dist, one_n_component, return_vals_filtered=return_vals_filtered)
                
                if MultiParamClass is None:
                    MultiParamClass = dataclass_from_dict("Params", returned_instance.args)
                    
                dict_key = MultiParamClass(**returned_instance.args)
                multi_param_result_dict[dict_key] = returned_instance
                
                #multi_param_result_dict[frozenset(returned_instance.args.items())] = returned_instance
    multi_param_result_dict = DataClassDict(multi_param_result_dict, MultiParamClass)
    return  locals()#multi_param_result_dict #locals() #{"embedding": u, "mapper": mapper}


def cluster_hdbscan(clusterable_embedding, min_cluster_size, viz_embedding_list, plot=True):
    print(f"min_cluster size: {min_cluster_size}")
    clusterer= hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
    ).fit(clusterable_embedding)
    labels = clusterer.fit_predict(clusterable_embedding)
    print(f"found {len(np.unique(labels))} clusters")
    clustered = (labels >= 0)
    frac_clustered = np.sum(clustered)/labels.shape[0]
    print(f"fraction clustered: {np.sum(clustered)/labels.shape[0]}")
    clusterer.condensed_tree_.plot(select_clusters=True,
                               selection_palette=sns.color_palette('deep', 8))
    
    for embedding in viz_embedding_list:
        
        if embedding.shape[1] == 3:
            fig = px.scatter_3d(x= embedding[:, 0],
                y= embedding[:, 1],
                z= embedding[:, 2],
                color = labels.astype("str"))
            display(fig)
            #.show()
#             ax = fig.add_subplot(111, projection='3d')
            
#             ax.scatter(embedding[~clustered][:, 0],
#                 embedding[~clustered][:, 1],
#                 embedding[~clustered][:, 2],
#                 c=(0.5, 0.5, 0.5),
#                 alpha=0.5)
#             ax.scatter(embedding[clustered][:, 0],
#                     embedding[clustered][:, 1],
#                     embedding[~clustered][:, 2],
#                     c=labels[clustered],
#                     cmap='Spectral')
        else:
            fig = px.scatter(x= embedding[:, 0],
                y= embedding[:, 1],
                color = labels.astype("str"))
            display(fig)
#             fig = plt.figure()
#             ax = fig.add_subplot(111)
#             ax.scatter(embedding[~clustered][:, 0],
#                 embedding[~clustered][:, 1],
#                 c=(0.5, 0.5, 0.5),
#                 s=10,
#                 alpha=0.5)
#             ax.scatter(embedding[clustered][:, 0],
#                     embedding[clustered][:, 1],
#                     c=labels[clustered].reshape(-1,1),
#                     s=10,
#                     cmap='Spectral')
            
#             plt.title(f"min_cluster_size = {min_cluster_size}", fontsize=18)
#             legend = ax.legend(*scatter.legend_elements())
#             ax.add_artist(legend)
#             plt.show()
        
    return {"labels":labels, "clusterer": clusterer}

def get_all_cluster_settings(fitted_hdbscan, embedding_used_to_cluster, unclustered_threshold=0.2, extra_cols_dict={}):
    '''
    unclustered_threshold: fraction of unclustered points allowed, if the number of points is more than this threshold, the setting is discarded
    '''
    test_label_dict = {}
    silhouette_scores = set()
    df_list = []
    linkage_tree = fitted_hdbscan.single_linkage_tree_
    condensed_tree_df = fitted_hdbscan.condensed_tree_.to_pandas().query("child_size > 1")
    for i, lambda_val in tqdm(enumerate(linkage_tree.to_pandas().sort_values("size", ascending = False).query("size > @condensed_tree_df.child_size.min()").distance.unique() - 0.01)):
        for child_size in sorted(condensed_tree_df["child_size"].unique() - 1):
            test_labels = fitted_hdbscan.single_linkage_tree_.get_clusters(lambda_val, min_cluster_size=2)
            # remove settings where alot is unclustered
            if (test_labels == -1).sum()/len(test_labels) > unclustered_threshold:
                continue
            try:
                #print(str(len(np.unique(test_labels))))
                test_silhouette_score = silhouette_score(embedding_used_to_cluster, test_labels)
            except ValueError:
                #print("skipped")
                continue

            if test_silhouette_score in silhouette_scores:
                continue

            col_name = str(len(np.unique(test_labels)))

            j = 0
            if col_name in test_label_dict:
                while f"{col_name}_{j}" in test_label_dict:
                    j+=1
                col_name = f"{col_name}_{j}"


            silhouette_scores.add(test_silhouette_score)
            #test_labels_df = pd.DataFrame(test_labels, columns=[f"{len(np.unique(test_labels))}_clusters_label"]).assign(**)
            df_list.append({"cluster_setting_num": i,
                            "col_name" : f"{col_name}_clusters_label",
                            "silhouette_score": test_silhouette_score,
                            "num_clusters": len(np.unique(test_labels)),
                            })#test_labels_df[[f"{len(np.unique(test_labels))}_clusters_label"]])                               
            test_label_dict[col_name] = test_labels
            #display(test_labels_df.head())
            #test_label_dict.append({f"{len(np.unique(test_labels))}_cluster_labels":list(test_labels), "silhouette_score": silhouette_score(test_clusteval_embed, test_labels) })


    all_labels_df = pd.DataFrame.from_dict(test_label_dict)

    #sort by number of clusters
    all_labels_df = all_labels_df[sorted(all_labels_df.columns, key=lambda x: tuple(map(int,x.split('_'))))].add_suffix("_clusters_label")
    all_labels_df = all_labels_df.assign(**extra_cols_dict)
    all_labels_df.index = embedding_used_to_cluster.index
    display(all_labels_df.head())
    cluster_metrics_df = pd.DataFrame(df_list)#.sort_values(["silhouette_score","num_clusters"], ascending= [False, True])
    
    return {"all_labels_df": all_labels_df, "cluster_metrics_df": cluster_metrics_df}

def get_cluster_defining_features(X, clustering_label, cluster_setting_name):
    """Need to provide X as features only and NO clustering label """
    cluster_names = np.unique(clustering_label)
    final_dict = {}
    all_cluster_info_mean_peaks_per_cluster = []
    
    for cluster_name in tqdm(cluster_names):
        if cluster_name == -1:
            continue
        print(cluster_name)
        final_dict[cluster_name] = {}
        cluster_one_v_all_labels = (clustering_label == cluster_name).astype(int)
        #use scale_pos_weight to address imbalance between clustering class vs rest
        with io.capture_output() as captured:
            all_OnevsAll_models_result_dict = repeat_train(X, cluster_one_v_all_labels,num_times=1000, different_train_test_split=True, name=cluster_setting_name, scale_pos_weight=cluster_one_v_all_labels.value_counts()[0]/cluster_one_v_all_labels.value_counts()[1], show_output=False)

        final_dict[cluster_name]["AUC_fig"] = all_OnevsAll_models_result_dict["fig"]

        #breakpoint()
        shap_mean_peaks_per_cluster_all_models = (pd.concat([result["shap_df"].assign(model_num=i) for i, result in enumerate(all_OnevsAll_models_result_dict["result_list"]) if result["metrics"]["test"]["AUC"] > 0.9]).reset_index())
        #explainer = shap.TreeExplainer(shap_mean_peaks_per_cluster_list[0][2])

        final_dict[cluster_name]["shap_summary_plot"]= shap.summary_plot(shap_mean_peaks_per_cluster_all_models.drop(columns=["model_num"]).groupby("index").mean().values, X[shap_mean_peaks_per_cluster_all_models.drop(columns=["index", "model_num"]).columns])

        aggregate_peak_info_mean_peaks_per_cluster = X[shap_mean_peaks_per_cluster_all_models.drop(columns=["index", "model_num"]).columns].assign(is_cluster = np.where(cluster_one_v_all_labels ==1, "cases_in_cluster", "cases_not_in_cluster")).groupby("is_cluster").agg(["mean", "median"]).swaplevel(-2,-1, axis=1)


        aggregate_peak_info_mean_peaks_per_cluster = pd.concat([aggregate_peak_info_mean_peaks_per_cluster["mean"].T.add_suffix("_mean"), aggregate_peak_info_mean_peaks_per_cluster["median"].T.add_suffix("_median")], axis=1)
        aggregate_peak_info_mean_peaks_per_cluster


        cluster_info_mean_peaks_per_cluster = shap_mean_peaks_per_cluster_all_models.drop_duplicates("model_num").drop(columns=["index", "model_num"]).count().to_frame()
        cluster_info_mean_peaks_per_cluster.columns = ["num_model_used_this_peak"]
        cluster_info_mean_peaks_per_cluster = cluster_info_mean_peaks_per_cluster.merge(aggregate_peak_info_mean_peaks_per_cluster, how = "outer", left_index = True, right_index=True)
        cluster_info_mean_peaks_per_cluster["cluster"] = cluster_name

        final_dict[cluster_name]["cluster_info_df"] = cluster_info_mean_peaks_per_cluster
        all_cluster_info_mean_peaks_per_cluster.append(cluster_info_mean_peaks_per_cluster)
        
    final_dict["combined_cluster_info_df"] = pd.concat(all_cluster_info_mean_peaks_per_cluster)
    final_dict["cluster_setting"] = cluster_setting_name
    return final_dict
