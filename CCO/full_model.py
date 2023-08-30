# Import packages
import itertools
import pandas as pd
import numpy as np

#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - Revvity/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_CCO_Design_skeleton_w_results.xlsx')
data = SFData

# Define Result column
result_column = 'RCC'

# Define simple terms
factors = data.columns.tolist()
factors.remove(result_column)

# Create a list of combinations for the factors ==> [(factor1,factor1), (factor1, factor2) , ... , (factorX, factorX)]
combination = [(x, y) for x, y in itertools.product(factors, repeat=2) if x <= y]  # Permits to avoid repetitions (if)

# Add new columns for each combination
for comb in combination:
    if comb[0] != comb[1]:
        new_col_name = comb[0] + ':' + comb[1]
        data[new_col_name] = data[comb[0]] * data[comb[1]]
    else:
        new_col_name = 'I(' + comb[0] + ' ** 2)'
        data[new_col_name] = data[comb[0]] * data[comb[1]]

# Transform result column
data[result_column] = np.log10(data[result_column])

# Move result column at the end without mentioning the whole order of column
new_order = list(data.columns.drop(result_column)) + [result_column]
data = data.reindex(columns=new_order)
data = data.rename(columns={result_column: f'Log10_{result_column}'})
data = data.astype('float64')

print(data)