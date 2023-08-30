# Import Packages
import pandas as pd
import numpy as np

# Import data
df = SFData
#df = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/FactorScreening_Design_skeleton_w_results.xlsx')

#Results definitition and management
results_table = pd.DataFrame()
result_to_analyze = 'RCC'
results_table[result_to_analyze] = np.log10(df[result_to_analyze])
df = df.drop(columns=[result_to_analyze])

# Result mean
result_mean = results_table[result_to_analyze].mean()

# dummies for Atmosphere
data_bisAt = pd.get_dummies(df['Atmosphere'], prefix= "Atmosphere", prefix_sep= "_")
data_bisAt = data_bisAt.replace(0, -1)
df = df.join(data_bisAt)
df = df.drop(columns="Atmosphere")


# Get the factors column name in a list
factors = df.columns.tolist()

df[result_to_analyze] = results_table[result_to_analyze]

# Instantiate the lists
minus_means = []
zero_means = []
plain_means = []

# Loop on all the columns except the last one which is the result
for col in df.columns[:-1]:

    # Calculate the mean of the results for the rows where the value in the column is 1
    mean_1 = df.loc[df[col] >= 1, result_to_analyze].mean()
    plain_means.append(mean_1)

    # Calculate the mean of the results for the rows where the value in the column is -1
    mean_neg_1 = df.loc[df[col] <= -1, result_to_analyze].mean()
    minus_means.append(mean_neg_1)

# Main_effect df creation
main_effect = pd.DataFrame()
main_effect["Terms"] = df.columns[:-1].tolist()
main_effect["Low"] = minus_means
main_effect["High"] = plain_means

# Pivot table 
melted_df = pd.melt(main_effect, id_vars='Terms', var_name='Mean Type', value_name='Mean')
print(melted_df)