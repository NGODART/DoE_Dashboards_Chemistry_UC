# Import packages
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Access the data (Design matrix with results)
data = sfdata
data = data.astype('float64')
#data = pd.read_excel('C:/Users/GodarN30918/OneDrive - Revvity/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/RSO_BB_Design_w_results - Copy.xlsx')

# Definition of the formula for the linear regression
formula = "RCC ~ Catalyst + Pyridine + Substrate + I(Pyridine ** 2) + I(Substrate ** 2) + Pyridine:Substrate"

# Fitting the MLR model
model = smf.ols(formula=formula, data=data).fit()

# Get the coefficients of every dependent variables
coefficients = model.params

# Prepare DataFrame for contour plot
x_min, x_max = data['Catalyst'].min(), data['Catalyst'].max()
y_min, y_max = data['Pyridine'].min(), data['Pyridine'].max()
resolution = int(resolutionDP)
#resolution = int(100)

# Prepare the meshgrids ( with real level of terms and with dimension of a blank canva for map chart (450*450))
# with canva dimension
xlist_500 = np.linspace(0, 450, resolution)
ylist_500 = np.linspace(0, 450, resolution)
X, Y = np.meshgrid(xlist_500, ylist_500)
Xrs = X.reshape(-1)
Yrs = Y.reshape(-1)

#with real levels
xlist = np.linspace(x_min, x_max, resolution)
ylist = np.linspace(y_min, y_max, resolution)
X_factor, Y_factor = np.meshgrid(xlist, ylist)
Xrs_factor = X_factor.reshape(-1)
Yrs_factor = Y_factor.reshape(-1)

# Creation of a dataframe to store all the meshgrid variables
df = pd.DataFrame({'Catalyst [eq]': Xrs_factor, 'Pyridine [eq]': Yrs_factor , 'X' : Xrs, 'Y' : Yrs  })

# Sort by value of Substrate, so it's in ascending order in plots
data = data.sort_values("Substrate")

# Create Z for each Substrate level
for substrate_value in data['Substrate'].unique():
    # for each substrate values, a new column Z will be added by building the regression formula with values in the meshgrid and predict values.
    Z_expression = f"{coefficients['Intercept']}"
    for term, coef in coefficients.items():
        if term != "Intercept":
            if ":" in term:
                term1, term2 = term.split(":")
                term_expression = f"{term1} * {term2} * {coef}"
            elif term.startswith("I(") and term.endswith(" ** 2)"):
                term = term.replace("I(", "").replace(" ** 2)", "")
                term_expression = f"{term} ** 2 * {coef}"
            else:
                term_expression = f"{term} * {coef}"

            Z_expression += f" + {term_expression}"
            print(Z_expression)

    Z_expression = Z_expression.replace("Catalyst", "Xrs_factor")
    Z_expression = Z_expression.replace("Pyridine", "Yrs_factor")
    Z_expression = Z_expression.replace("Substrate", f"{substrate_value}")

    print(Z_expression)
    Z = eval(Z_expression)
    
    # Apply the expression to create a new column.
    df[f"RCC {int(substrate_value)} µmol Substrate"] = Z


print(df)

