# Import Packages
import pandas as pd
import numpy as np

# Import data
df_original_table = SFData
#df_original_table = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_CCO_Design_skeleton_w_results.xlsx')

#Results definitition and management
results_table = pd.DataFrame()
result_to_analyze = 'RCC'
results_table[result_to_analyze] = np.log10(df_original_table[result_to_analyze])
result_mean = results_table[result_to_analyze].mean()
df_original_table = df_original_table.drop(columns=[result_to_analyze])

# Get the factors column name in a list
factors = df_original_table.columns.tolist()

# should remove result column name from the factors list than create a df to store the column and delete the column from the original one before adding it again (I know)
df_original_table[result_to_analyze] = results_table[result_to_analyze]

# Instantiate lists
minus_means = []
zero_means = []
plain_means = []

# Loop on all the columns except the last one which is the result
for col in df_original_table.columns[:-1]:

    # Calculate the mean of the results for the rows where the value in the column is 1
    mean_1 = df_original_table.loc[df_original_table[col] >= 1, result_to_analyze].mean()
    plain_means.append(mean_1)

    # Calculate the mean of the results for the rows where the value in the column is 0
    mean_0 = df_original_table.loc[df_original_table[col] == 0, result_to_analyze].mean()
    zero_means.append(mean_0)

    # Calculate the mean of the results for the rows where the value in the column is -1
    mean_neg_1 = df_original_table.loc[df_original_table[col] <= -1, result_to_analyze].mean()
    minus_means.append(mean_neg_1)

# Main_effect df creation
interaction_table = pd.DataFrame()
interaction_table["Terms"] = df_original_table.columns[:-1].tolist()
interaction_table["Low"] = minus_means
interaction_table["Center"] = zero_means
interaction_table["High"] = plain_means

# Pivot table 
melted_df = pd.melt(interaction_table, id_vars='Terms', var_name='Mean Type', value_name='Mean')
print(melted_df)