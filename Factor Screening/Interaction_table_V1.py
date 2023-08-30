# Import Packages
import numpy as np
import pandas as pd
import itertools

# Import data
df = SFData
#df = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/FactorScreening_Design_skeleton_w_results.xlsx')

# Replace coding by Atm_Air
df['Atmosphere_Air'] = df['Atmosphere_code']
df = df.drop(columns=["Atmosphere_code"])

# Define result column
Res_column = "RCC"

# Calculate RCC mean
Log10RCCMean= np.log10(df[Res_column]).mean()

# Manage RCC column in another DF (not beautiful - sry)
results_table = pd.DataFrame()
results_table[Res_column]= np.log10(df[Res_column])
df = df.drop(columns=[Res_column])

# List to store the column values for the new DataFrame
interaction = []
level_interaction = []
mean_rcc = []

# Get all possible combinations of factors
factors = df.columns.tolist()
combination = list(itertools.combinations(factors, 2))
print(combination)

# Add new columns for each combination
for comb in combination:
    if comb[0] != comb[1]:
        new_col_name = comb[0] + ':' + comb[1]
        df[new_col_name] = df[comb[0]] * df[comb[1]]
    else:
        new_col_name = 'I(' + comb[0] + ' ** 2)'
        df[new_col_name] = df[comb[0]] * df[comb[1]]

# Only keep the combinations
df = df.drop(columns = factors)

# Return of the reuyslt column in the initial df (sry again)
df[Res_column]= results_table[Res_column]

# Instantiate lists
minus_means = []
plain_means = []

# Loop on all the columns except the last one which is the result
for col in df.columns[:-1]:

    # Calculate the mean of the results for the rows where the value in the column is 1
    mean_1 = df.loc[df[col] >= 1, Res_column].mean()
    plain_means.append(mean_1)


    # Calculate the mean of the results for the rows where the value in the column is -1
    mean_neg_1 = df.loc[df[col] <= -1, Res_column].mean()
    minus_means.append(mean_neg_1)

# Creation of the interaction table df
interaction_table = pd.DataFrame()
interaction_table["Interaction"] = df.columns[:-1].tolist()
interaction_table["Low"] = minus_means
interaction_table["High"] = plain_means

# Pivot table
melted_df = pd.melt(interaction_table, id_vars='Interaction', var_name='Interaction Level', value_name='Mean Response')


# Print the new DataFrame
print(melted_df)