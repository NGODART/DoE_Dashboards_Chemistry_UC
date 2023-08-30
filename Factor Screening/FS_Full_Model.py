# Packages Import
import itertools
import pandas as pd
import numpy as np

#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/FactorScreening_Design_skeleton_w_results.xlsx')
data = SFData

# Define result column
result_column = 'RCC'

# Create a new pandas DF with Atmosphere dummies and join tables
data_bisAt = pd.get_dummies(data['Atmosphere'], prefix= "Atmosphere", prefix_sep= "_" )
data = data.join(data_bisAt)

# Remove previously used column
data = data.drop(columns="Atmosphere")
data = data.drop(columns="Atmosphere_code")

# Create a new pandas DF with Block dummies and join tables
data_bisBlo = pd.get_dummies(data["Block"], prefix= "Block", prefix_sep= "_")
data = data.join(data_bisBlo)

# Remove previously used column
data = data.drop(columns="Block")

# Create factor list  from df columns and remove the result column from the list
factors = data.columns.tolist()
factors.remove(result_column)

#remove blocks from interactions
factors_filtered = [factor for factor in factors if not factor.startswith('Block_')]

# Create a list of combinations for the factors ==> [(factor1,factor1), (factor1, factor2) , ... , (factorX, factorX)]
combination = [(x, y) for x, y in itertools.product(factors_filtered, repeat=2) if x <= y]  # Permits to avoid repetitions (if)

# Add new columns for each combination
for comb in combination:
    if not ((comb[0].startswith('Atmos')) and (comb[1].startswith('Atmos'))) : # avoid atmos square terms
        if comb[0] != comb[1]:
            new_col_name = comb[0] + ':' + comb[1]
            data[new_col_name] = data[comb[0]] * data[comb[1]]
        else:
            new_col_name = 'I(' + comb[0] + ' ** 2)'
            data[new_col_name] = data[comb[0]] * data[comb[1]]


# Transform results according to the article
y = np.log10(data[result_column])
data[result_column] = np.log10(data[result_column])


# Move Result column on the last position in the table
new_order = list(data.columns.drop(result_column)) + [result_column]
data = data.reindex(columns=new_order)

# Rename column and put all the table as float
data = data.rename(columns={result_column: f'Log10_{result_column}'})
data = data.astype('float64')

print(data)