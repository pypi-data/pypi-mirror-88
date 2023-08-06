# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .nodes import split_data
from ._00_data_cleaning import (
    fix_chipseq_df_columns,
    transpose_case_row_col_peak,
    process_sample_covs,
    make_processed_datasets,
    make_ML_matrix,
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_data,
                ["example_iris_data", "params:example_test_data_ratio"],
                dict(
                    train_x="example_train_x",
                    train_y="example_train_y",
                    test_x="example_test_x",
                    test_y="example_test_y",
                ),
            ),
            node(
                func = fix_chipseq_df_columns,
                inputs = ["ChIP_original_wrong_cols"],
                outputs = "ChIP_correct_cols",
                name = "Fix unnamed/shifted columns in ChIP data"
            ),
            node(
                func = transpose_case_row_col_peak,
                inputs = ["ChIP_correct_cols"],
                outputs = "ChIP_correct_cols_transposed",
                name = "Transpose row = sample, col = peaks"
            ),
            node(
                func = process_sample_covs,
                inputs = ["sample_covs"],
                outputs = "sample_covs_cleaned",
                name = "Clean covs data entry mistakes"
            ),
            
            node(
                func = make_processed_datasets,
                inputs = ["sample_covs_cleaned", "ChIP_correct_cols_transposed", "params:important_covs" ],
                outputs = ["sample_covs_cleaned_inherent_samples_only", "important_covs_and_cc_status"],
                name = "Create covs datasets with only samples in ChIP data and important covs"
            ),
            
            node(
                func = make_ML_matrix,
                inputs = ["important_covs_and_cc_status", "ChIP_correct_cols_transposed"],
                outputs = ["important_covs_and_cc_status_dummified", "ML_X_y_matrix"],
                name = "Dummify category vars and join ChIP + covs"
            ),
            
            
        ]
    )
