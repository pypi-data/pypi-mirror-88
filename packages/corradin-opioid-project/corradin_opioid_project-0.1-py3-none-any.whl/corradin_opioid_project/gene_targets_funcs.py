import pandas as pd
import pybedtools
import numpy as np

def get_gene_targets(peak_list, region_split_char, gene_target_file):
    bed_info = pd.DataFrame(peak_list, columns = ["peak"])
    bed_info[["chromosome", "start", "stop"]] = bed_info.peak.str.split(region_split_char, expand = True)
    bed_info = bed_info.drop(columns = "peak")
    display(bed_info.head())

    bed_file = pybedtools.BedTool.from_dataframe(bed_info)
    intersected = bed_file.intersect(gene_target_file, wao=True).to_dataframe().query("score != -1")
    display(intersected.head())

    intersected_exploded = intersected.assign(thickStart=intersected.thickStart.str.split(";")).explode("thickStart")
    intersected_exploded.drop_duplicates(["chrom", "start", "end", "thickStart"])
    return intersected_exploded


class PeakToGeneMapper():
    
    def __init__(self, peaks_df, *, split_char, hiC_file_path):
        self.peaks_df = peaks_df
        self.split_char = split_char
        self.hiC_file_path = hiC_file_path
    
    @classmethod
    def get_mapping_dict(cls, peaks_n_genes):
        mapping_dict = peaks_n_genes[["peak", "peak_or_gene"]].to_dict(orient="index")
        one_peak_multi_gene_mapping_dict = {}

        #make sure that peak can be associated with multiple genes:
        for k, v in mapping_dict.items():
            peak = v["peak"]
            gene = v["peak_or_gene"]
            if peak not in one_peak_multi_gene_mapping_dict:
                one_peak_multi_gene_mapping_dict[peak] = gene
            else:
                one_peak_multi_gene_mapping_dict[peak] = f"{one_peak_multi_gene_mapping_dict[peak]}_{gene}"
        return one_peak_multi_gene_mapping_dict
    
    @property
    def gene_targets_raw(self):
        print("all the genes from raw intersectBed with peaks")
        gene_targets_raw = get_gene_targets(self.peaks_df.index, self.split_char, self.hiC_file_path)
        return gene_targets_raw
        
    @property
    def peaks_n_genes_df(self):
        print("all genes + peaks that couldn't be mapped to genes")
        genes = self.gene_targets_raw.copy()
        genes["peak"] = genes[["chrom", "start", "end"]].astype(str).apply("_".join, axis=1)
        genes = genes.set_index("peak")
        peaks_n_genes = self.peaks_df.merge(genes, left_index=True, right_index=True, how="outer")
        peaks_n_genes.index.name = "peak"
        peaks_n_genes = peaks_n_genes.assign(peak_or_gene = np.where(peaks_n_genes["thickStart"].isna(), peaks_n_genes.index, peaks_n_genes["thickStart"]))
        one_peak_multi_gene_mapping_dict = self.__class__.get_mapping_dict(peaks_n_genes.reset_index())
        peaks_n_genes["peak_and_all_connected_genes"] = peaks_n_genes.reset_index()["peak"].replace(one_peak_multi_gene_mapping_dict).values
        peaks_n_genes["found_gene"] = np.where(peaks_n_genes["thickStart"].notna(), 1, 0)
        peaks_n_genes = peaks_n_genes.drop_duplicates(["model_num", "peak_and_all_connected_genes"])
        return peaks_n_genes
    
    @property
    def unique_genes_per_model_df(self):
        unique_genes_per_model_df = self.peaks_n_genes_df.groupby("model_num")["thickStart"].unique().explode().to_frame()
        return unique_genes_per_model_df
    
    @property
    def gene_frequency_df(self):
        gene_frequency_df = self.unique_genes_per_model_df["thickStart"].value_counts().to_frame()
        return gene_frequency_df
    
    
        