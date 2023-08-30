#Import Packages 
import pandas as pd
from statsmodels.stats.anova import anova_lm
import statsmodels.formula.api as smf
import numpy as np

# Import Data
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/full_model_FS.xlsx')
data = SFData
data = data.astype('float64')

# Define result column
result_column = 'Log10_RCC'

# Import selected columns
selectedColumnsreceive = selectedColumns
x_columns = selectedColumnsreceive.split(',')
x = data[x_columns]

# Fit the model with selected columns
formula = f'{result_column} ~ {" + ".join(x_columns)}'
modelfit = smf.ols(formula=formula, data=data).fit()

# Summary table creation
table = modelfit.summary().tables[1]
Simplified_summary = table.data
column_names = Simplified_summary[0]
column_names[0] = "Terms"
simplesummary = [row[:1] + [float(value) for value in row[1:]] for row in Simplified_summary[1:]]
simplesummary = pd.DataFrame(simplesummary, columns=column_names)
print(f" Table de Coefficients: \n  {simplesummary}")

# Rsquared calculation
Rsquared = modelfit.rsquared
print(f"Rsquared : {Rsquared}")

# Initialize variables for LOOCV
n = len(data)
mse = np.zeros(n)

# Perform LOOCV
for i in range(n):
    # Fit model without observation i
    fit_data = data.drop(i)
    fit = smf.ols(formula, data=fit_data).fit()

    # Predict value of observation i
    pred = fit.predict(data.iloc[[i]])

    # Calculate squared difference between predicted and actual value
    mse[i] = (pred - data.loc[i, result_column])**2

# Calculate Q2
variance = data[result_column].var()

Q2 = 1 - np.mean(mse) / variance

print(f"Qsquared : {Q2}")
