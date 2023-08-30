#Import packages
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
import warnings

# Disable warnings
warnings.simplefilter("ignore")

# Import data
data = sfData
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_CCO_Design_skeleton_w_results.xlsx')
data = data.astype('float64')

# Define result column
#result_column = ResColumn
result_column = "RCC"

# Turn RCC into Log10 RCC
data[result_column]= np.log10(data[result_column])

# Create list of factors
factors = data.columns.tolist()
factors.remove(result_column)

# Create a list of combinations for the factors
combination = [(x, y) for x, y in itertools.product(factors, repeat=2) if x <= y]

# Create a copy of the list of factors
simple_factors = factors.copy()

# Add new columns for each combination
for comb in combination:
    if comb[0] != comb[1]:
        new_col_name = f"{comb[0]}:{comb[1]}"
        factors.append(new_col_name)
        data[new_col_name] = data[comb[0]] * data[comb[1]]

    else:  #We can't use it in DSD
        new_col_name = f"I({comb[0]} ** 2)"
        factors.append(new_col_name)
        data[new_col_name] = data[comb[0]] * data[comb[1]]

# Instantiate the list of factors for stepwise
x_columns = factors

# Result definition
y = data[result_column]

# Define alpha 
alpha = 0.05

def get_stats(y, x_columns):
    # MLR and summary table
    x = sm.add_constant(data[x_columns].astype(float).fillna(0))
    y = y.astype(float).fillna(0)
    results = sm.OLS(y, x).fit()
    table = results.summary().tables[1]
    summary_data = table.data[1:]
    
    # Saving factor names and p values
    col1 = [item[0] for item in summary_data]
    colvalue = [item[4] for item in summary_data]
    col2 = [float(i) for i in colvalue]
    
    # Creating a dataframe with this columns (easier to manipulate)
    df = pd.DataFrame({'X_column': x_columns, 'P>|t|': col2[1:]})
    df.iloc[0, 0] = 'const'
    df_i = df
    
    # Discard simple terms from the stepwise ( we keep them)
    df_i.drop(range(0, len(simple_factors)), inplace=True)
    
    # Verify if every p value is above alpha
    valid = (df_i['P>|t|'] < alpha).all()

    # if valid, then return the summary table, the model (result) and the columns in the model
    if valid:
        return table, results, x_columns

    else:
        max_value = df_i['P>|t|'].max()
        value = df_i['X_column'].where(df_i['P>|t|'] == max_value).dropna().iloc[0]
        x_col_copy = x_columns
        x_col_copy.remove(value)
        # run function again with the new list of factors
        return get_stats(y, x_col_copy)

# Save the result of the function in a variable (ok)
ok = get_stats(y, x_columns)

# Get simplified summary and turn it in a DF
Simplified_summary = ok[0].data
column_names = Simplified_summary[0]
column_names[0] = "Terms"
simplesummary = [row[:1] + [float(value) for value in row[1:]] for row in Simplified_summary[1:]]
df = pd.DataFrame(simplesummary, columns=column_names)
print(df)

# List of significant terms
SignficantTerms = str(ok[2])

# Calculate Rsquared, residuals, std residuals, and fitted values
Rsquared = ok[1].rsquared
print(Rsquared)
residuals = ok[1].resid
Pearson_residuals = ok[1].resid_pearson
Fittedvalues = ok[1].fittedvalues

# Generate formula for LOOCV
formula = f'{result_column} ~ {" + ".join(ok[2])}'

# Initialize variables
n = len(data)
mse = np.zeros(n)

# Perform LOOCV
for i in range(n):
    # Fit model without observation i
    fit_data = data.drop(i)
    fit = sm.formula.ols(formula, data=fit_data).fit()

    # Predict value of observation i
    pred = fit.predict(data.iloc[[i]])

    # Calculate squared difference between predicted and actual value
    mse[i] = (pred - data.loc[i, "RCC"])**2


# Calculate Q2
variance = data[result_column].var()
Q2 = 1 - np.mean(mse) / variance

print(Q2)