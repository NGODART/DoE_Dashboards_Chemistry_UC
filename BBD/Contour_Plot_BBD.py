# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from matplotlib.patheffects import withStroke
from io import BytesIO

######### DATA WRANGLING AND TRANSFORMATION #########

# Access the data (Design matrix with results)
data = ModelData

# Add new columns for MLR
data["Pyridine^2"] = data["Pyridine"] ** 2
data["Substrate^2"] = data["Substrate"] ** 2
data["Substrate*Pyridine"] = data["Substrate"] * data["Pyridine"]

######### LINEAR REGRESSION #########

# Definition of the independent and dependent variables
independent_vars = data[['Catalyst', 'Pyridine', 'Substrate', 'Pyridine^2', 'Substrate^2', 'Substrate*Pyridine']]
independent_vars = sm.add_constant(independent_vars)
dependent_var = data['RCC']

independent_vars, dependent_var = np.array(independent_vars, dtype=float), np.array(dependent_var, dtype=float)

# Fitting the MLR model
model = sm.OLS(dependent_var, independent_vars).fit()

# Get the coefficients of every dependent variables
coefficients = model.params
coefficients = pd.DataFrame(coefficients)

# Extract coefficients from summary as Float
Coef_intercept = coefficients.iloc[0,0]
Coef_Catalyst = coefficients.iloc[1,0]
Coef_Pyridine = coefficients.iloc[2,0]
Coef_Substrate = coefficients.iloc[3,0]
Coef_Pyridine2 = coefficients.iloc[4,0]
Coef_Substrate2 = coefficients.iloc[5,0]
Coef_Substrate_Pyridine = coefficients.iloc[6,0]

######### PREPARATION FOR THE CONTOUR PLOT #########

# Sort by value of Substrate, so it's in ascending order in plots
data = data.sort_values("Substrate")

# Define the levels of Substrate
substrate_values = data["Substrate"].unique()

# Definition of the meshgrid dimensions
x_min, x_max = data['Catalyst'].min(), data['Catalyst'].max()
y_min, y_max = data['Pyridine'].min(), data['Pyridine'].max()
resolution = 100

# Creation of the meshgrid
xlist = np.linspace(x_min, x_max, resolution)
ylist = np.linspace(y_min, y_max, resolution)
X, Y = np.meshgrid(xlist, ylist)

######### CREATION OF CONTOUR PLOTS #########

# Create a figure and subplots for each value of the independent variable
fig, axs = plt.subplots(1, len(substrate_values), figsize=(12, 4), constrained_layout=True)

# Instanciate levels zmin and zmax
zmin = zmax = None

# First iteration of the prediction to determine the levels to apply.
for i, ax in enumerate(axs):

    # Instantiate the value of Substrate in the prediction of Z
    substrate_value = substrate_values[i]

    # Calculate Z with the MLR equation
    Z = Coef_intercept + (
                Coef_Catalyst * X + Coef_Pyridine * Y + Coef_Pyridine2 * Y ** 2 + Coef_Substrate_Pyridine * substrate_value * Y + Coef_Substrate2 * substrate_value ** 2 + Coef_Substrate * substrate_value)

    # Update zmin and zmax
    if (zmin is None) or (zmin > Z.min()):
        zmin = Z.min()
    if (zmax is None) or (zmax < Z.max()):
        zmax = Z.max()

# Second iteration of the prediction to plot the contour plots.
for i, ax in enumerate(axs):
    # Instantiate the value of Substrate in the prediction of Z
    substrate_value = substrate_values[i]

    # Calculate Z with the MLR equation
    Z = Coef_intercept + (
                Coef_Catalyst * X + Coef_Pyridine * Y + Coef_Pyridine2 * Y ** 2 + Coef_Substrate_Pyridine * substrate_value * Y + Coef_Substrate2 * substrate_value ** 2 + Coef_Substrate * substrate_value)

    # Estimate levels (one every 10 units)
    levels = np.arange(np.floor(zmin / 10) * 10, np.ceil(zmax / 10) * 10 + 1, 10)

    # Add the current plot as a subplot in the general fig
    ax = axs[i]

    # Generation of the plot
    cp = ax.contourf(X, Y, Z, levels=levels, cmap="turbo")
    cs = ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.5)
    labels = ax.clabel(cs, inline=True, fontsize=10, fmt='%1.1f')

    # Add white borders to contour labels
    white_border = withStroke(linewidth=3, foreground='white')
    for label in labels:
        label.set_path_effects([white_border])

    # Set axis names
    ax.set_title(f'Substrate Load [µmol] = {substrate_value}')
    ax.set_xlabel('Catalyst Load [Eq]')
    if i == 0 :
        ax.set_ylabel('Pyridine Load [Eq]')
    else :
        ax.set_yticklabels([])

# Create a binary stream
buf = BytesIO()

# Plot the result
cbar = fig.colorbar(axs[-1].contourf(X, Y, Z, levels=levels, cmap='turbo'))
cbar.set_label('RCC [%]')

# Save the plot as a PDF
plt.savefig(buf, format='png')

# Get the contents of the stream as a binary string
plot_data = buf.getvalue()


