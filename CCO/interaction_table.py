# Import package
import numpy as np
import pandas as pd
import itertools

# Import data
df = SFData
#df = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_CCO_Design_skeleton_w_results.xlsx')

# Calculate mean result
Log10RCCMean= np.log10(df["RCC"]).mean()

# List to store the column values for the new DataFrame
term1 = []
term2 = []
level_term1 = []
level_term2 = []
mean_rcc = []

# Get all possible combinations of factors
Res_column = "RCC"
factors = df.columns.tolist()
factors.remove(Res_column)
factor_combinations = list(itertools.combinations(factors, 2))

# Loop through each factor combination
for factor_pair in factor_combinations:
    factor1, factor2 = factor_pair

    # Get all possible combinations of factor levels
    levels1 = df[factor1].unique().tolist()
    # if 0 in levels1:
    #     levels1.remove(0)
    levels2 = df[factor2].unique().tolist()
    level_combinations = list(itertools.product(levels1,levels2))

    # Loop through each level combination
    for level_pair in level_combinations:
        level1, level2 = level_pair

        # Filter the DataFrame based on the factor and level combinations
        filtered_df = df[(df[factor1] == level1) & (df[factor2] == level2)]

        # Calculate the mean of RCC for the filtered data
        mean_rcc_value = np.log10(filtered_df[Res_column]).mean()

        # Append the column values to the respective lists
        term1.append(factor1)
        term2.append(factor2)
        level_term1.append(level1)
        level_term2.append(level2)
        mean_rcc.append(mean_rcc_value)

# Create the new DataFrame
new_data = {
    'Term 1': term1,
    'Term 2': term2,
    'Level Term 1': level_term1,
    'Level Term 2': level_term2,
    'Mean RCC': mean_rcc
}

new_df = pd.DataFrame(new_data).dropna()

# Loop through each row in the DataFrame
for index, row in new_df.iterrows():
    # Check and transform level values
    if row['Level Term 1'] >= 1:
        new_df.at[index, 'Level Term 1'] = 'High'
    elif row['Level Term 1'] <= -1:
        new_df.at[index, 'Level Term 1'] = 'Low'
    else:
        new_df.at[index, 'Level Term 1'] = 'Center'

    if row['Level Term 2'] >= 1:
        new_df.at[index, 'Level Term 2'] = 'High'
    elif row['Level Term 2'] <= -1:
        new_df.at[index, 'Level Term 2'] = 'Low'
    else:
        new_df.at[index, 'Level Term 2'] = 'Center'


# Print the new DataFrame
print(new_df)