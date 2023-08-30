# Import packages
import itertools
import pandas as pd
import statsmodels.api as sm
import numpy as np

# Import data
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - Revvity/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/FactorScreening_Design_skeleton_w_results.xlsx')
data = SFData

# Define result column
result_column = 'RCC'

# Get atmosphere dummies
data_bis = pd.get_dummies(data['Atmosphere'], prefix= "Atmosphere", prefix_sep= "_")
data = data.join(data_bis)
data = data.drop(columns="Atmosphere")

# Get block dummies
data_bis = pd.get_dummies(data["Block"], prefix= "Block", prefix_sep= "_")
data = data.join(data_bis)
data = data.drop(columns="Block")

# Transtype to float
data = data.astype('float64')

# Set factor list
factors = data.columns.tolist()
factors.remove(result_column)

# Scale and centering (important to find same results as in the article for some reason)
mean = data[factors].mean()
std = data[factors].std()
data[factors] = (data[factors] - mean) / std

#remove blocks from interactions
factors_filtered = [factor for factor in factors if not factor.startswith('Block_')]

# Create a list of combinations for the factors ==> [(factor1,factor1), (factor1, factor2) , ... , (factorX, factorX)]
combination = [(x, y) for x, y in itertools.product(factors_filtered, repeat=2) if x <= y]  # Permits to avoid repetitions (if)

# Add new columns for each combination
for comb in combination:
    if not ((comb[0].startswith('Atmos')) and (comb[1].startswith('Atmos'))):  # avoid atmos square terms
        if comb[0] != comb[1]:
            new_col_name = f"{comb[0]}:{comb[1]}"
            data[new_col_name] = data[comb[0]] * data[comb[1]]

        else:  #We can't use it in DSD
            new_col_name = f"I({comb[0]}**2)"
            data[new_col_name] = data[comb[0]] * data[comb[1]]

# Instantiate X_columns for the stepwise
x_columns = data.columns.tolist()

# Remove the result column from the list
x_columns.remove(result_column)

# Transform results
y = np.log10(data[result_column])

# Instantiate alpha for level of significance
alpha = 0.05

def get_stats(x_columns):
    "will return a coefficient table, the model fitted, and the list of independent variables"
    # MLR and summary table
    x = data[x_columns]
    results = sm.OLS(y, sm.add_constant(x)).fit()
    table = results.summary().tables[1]
    summary_data = table.data[1:]
    
    # Saving factor names and p values
    col1 = [item[0] for item in summary_data]
    colvalue = [item[4] for item in summary_data]
    col2 = [float(i) for i in colvalue]
    
    # Creating a dataframe with this columns (easier to manipulate)
    df = pd.DataFrame({'X_column': col1, 'P>|t|': col2})
    df_i = df
    df_i.drop(range(0, len(factors)+1), inplace=True) # const + B2, B3, B4 (4 columns to save)
    
    # Verify if every p value is above alpha
    valid = (df_i['P>|t|'] < alpha).all()
    
    # if valid, then return the summary table, the model (result) and the columns in the model
    if valid:
        return (table, results, x_columns)
        
    # else, discard the interaction with the highest p value
    else:
        max_value = df_i['P>|t|'].max()
        value = df_i['X_column'].where(df_i['P>|t|'] == max_value).dropna().iloc[0]
        x_col_copy = x_columns
        x_col_copy.remove(value)
        # run function again with the new list of factors 
        return get_stats(x_col_copy)

# Save the result of the function in a variable (stepwiseRes)
stepwiseRes = get_stats(x_columns)

# Get simplified summary and turn it in a DF
Simplified_summary = stepwiseRes[0].data
column_names = Simplified_summary[0]
column_names[0] = "Terms"
simplesummary = [row[:1] + [float(value) for value in row[1:]] for row in Simplified_summary[1:]]
simplesummary = pd.DataFrame(simplesummary, columns=column_names)


print(simplesummary)