# Import packages
import itertools
import pandas as pd
from pandas import DataFrame

# Import data
df_original_table: DataFrame = SFData

# resulmt management (not clean)
results_table = pd.DataFrame()
result_to_analyze = 'RCC'
results_table[result_to_analyze] = df_original_table[result_to_analyze]
df_original_table = df_original_table.drop(columns=[result_to_analyze])

# RCC mean calculation 
result_mean = results_table[result_to_analyze].mean()

# Get the factors column name in a list
factors = df_original_table.columns.tolist()

# Result added to the original table 
df_original_table[result_to_analyze] = results_table[result_to_analyze]

# Instantiate the lists
minus_means = []
zero_means = []
plain_means = []

# Loop on all the columns except the last one which is the result
for col in df_original_table.columns[:-1]:

    # Calculate the mean of the results for the rows where the value in the column is 1
    mean_1 = df_original_table.loc[df_original_table[col] == 1, result_to_analyze].mean()
    plain_means.append(mean_1)

    # Calculate the mean of the results for the rows where the value in the column is 0
    mean_0 = df_original_table.loc[df_original_table[col] == 0, result_to_analyze].mean()
    zero_means.append(mean_0)

    # Calculate the mean of the results for the rows where the value in the column is -1
    mean_neg_1 = df_original_table.loc[df_original_table[col] == -1, result_to_analyze].mean()
    minus_means.append(mean_neg_1)

# Create new df
interaction_table = pd.DataFrame()
interaction_table["Terms"] = df_original_table.columns[:-1].tolist()
interaction_table["-1"] = minus_means
interaction_table["0"] = zero_means
interaction_table["+1"] = plain_means

print(interaction_table)

# Pivot table
melted_df = pd.melt(interaction_table, id_vars='Terms', var_name='Mean Type', value_name='Mean')