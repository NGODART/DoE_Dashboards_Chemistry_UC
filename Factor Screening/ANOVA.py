# Import Packages
import pandas as pd
from statsmodels.stats.anova import anova_lm
import statsmodels.formula.api as smf
import numpy as np

# Import data
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/full_model_FS.xlsx')
data = SFData
data = data.astype('float64')

# Define result column
result_column = 'Log10_RCC'

# Import selected column 
selectedColumnsreceive = selectedColumns
x_columns = selectedColumnsreceive.split(',')
x = data[x_columns]

# Fit the model with selected columns
formula = f'{result_column} ~ {" + ".join(x_columns)}'
modelfit = smf.ols(formula=formula, data=data).fit()

# Calculate residuals, std residuals and fittedvalues
residuals = modelfit.resid
pearson_residuals = modelfit.resid_pearson
fittedvalues = modelfit.fittedvalues
print(fittedvalues)

# Perform ANOVA and obtain the table
anova_table = anova_lm(modelfit)
anova_table = anova_table.rename_axis("Terms")
anova_table = anova_table.reset_index()

print(f"Table d'ANOVA :\n {anova_table}")