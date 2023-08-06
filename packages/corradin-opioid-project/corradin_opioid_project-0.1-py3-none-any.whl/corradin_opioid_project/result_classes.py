import pandas as pd

class CVMultiPeakSetResult:
    def __init__(self, result):
        self.result = result
        
    @property
    def all_removed_peaks_df(self):
        all_removed_peaks_list = [result["best_feature_set"] for result in self.result["removed_peaks"]]
        all_removed_peaks_df = pd.concat(all_removed_peaks_list)
        return all_removed_peaks_df
    @property
    def all_models_all_best_peak_sets_auc_summarized(self):
        all_models_all_best_peak_sets_auc_summarized = pd.concat([result["cross_val_results_df_summarized"].head(1).assign(model_num = i) for i, result in enumerate(self.result["removed_peaks"])])
        all_models_all_best_peak_sets_auc_summarized["best_peak_set"] = all_models_all_best_peak_sets_auc_summarized.index
        return all_models_all_best_peak_sets_auc_summarized
    @property
    def all_models_all_peak_sets_cv_auc(self):
        all_models_all_peak_sets_cv_auc = pd.concat([result["cross_val_results_df"].assign(model_num = i) for i, result in enumerate(self.result["removed_peaks"])])
        return all_models_all_peak_sets_cv_auc
    @property
    def all_models_best_peak_sets_cv_auc(self):
        all_models_best_peak_sets_cv_auc = self.all_models_all_peak_sets_cv_auc.merge(self.all_models_all_best_peak_sets_auc_summarized[["model_num", "best_peak_set"]]).query("peak_set == best_peak_set ")
        return all_models_best_peak_sets_cv_auc
    
    def get_model_result(self, model_num):
        return self.result["result_list"][model_num]
    
    #all peak sets for a specific model
    def get_peak_sets_list(self, model_num):
        return self.get_model_result(model_num)["peak_set_list"]