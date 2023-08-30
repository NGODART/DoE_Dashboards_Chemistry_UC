# Import packages
import pandas as pd
import statsmodels.formula.api as smf
import re
from statsmodels.stats.anova import anova_lm

# Import and transform data
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - PerkinElmer Inc/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_BB_Design_w_results - Copy.xlsx')
data = SFData
data = data.astype('float64')
data = data.rename(columns=lambda x: x.replace(' ', '_'))

# Define and transform result column
ResColumn = "RCC"
result_column = ResColumn.replace(' ', '_')

# Import significant factors
SignificantFactors = eval(SignificantFactorsList)
#SignificantFactors = ['Catalyst', 'Substrate', 'Pyridine', 'I(Substrate ** 2)', 'Pyridine:Substrate', 'I(Pyridine ** 2)']

for i in range(len(SignificantFactors)):
    # Replace spaces with underscores in the string
    # Replace spaces with underscores except before and after **
    SignificantFactors[i] = re.sub(r'(?<!\*)\s+(?!\*)', '_', SignificantFactors[i])

# Fit the full model
formula = f'{result_column} ~ {" + ".join(SignificantFactors)}'
model = smf.ols(formula=formula, data=data).fit()

# Perform ANOVA and obtain the table
anova_table = anova_lm(model)
anova_table = anova_table.rename_axis("Terms")
anova_table = anova_table.reset_index()