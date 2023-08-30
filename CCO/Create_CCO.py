import pandas as pd
from pyDOE2 import ccdesign


def createCCO():
    # Define the number of factors and their ranges
    factors = ["Catalyst", "Pyridine", "Substrate"]
    low_values = [1, 10, 10]
    high_values = [4, 40, 30]

    # Calculate alpha from formula
    levels = 2
    nbcenter = 3
    T= 2*len(factors)+nbcenter
    F= levels ** len(factors)
    alpha = ((((F + T) ** (1 / 2) - F ** (1 / 2)) ** 2) * (F / 4)) ** (1 / 4)

    # Generate the central composite design matrix
    ccd_matrix = ccdesign(len(factors), center=(0, nbcenter), alpha="orthogonal")

    # Convert the design matrix to a Pandas DataFrame
    ccd_df = pd.DataFrame(ccd_matrix, columns=factors)

    for col in ccd_df.columns:
        # Apply corrected alpha
        ccd_df.loc[ccd_df[col] > 1, col] = alpha
        ccd_df.loc[ccd_df[col] < -1, col] = -alpha
        
    ccd_df_skeleton = ccd_df.copy()

    # Apply correct levels
    for i, factor in enumerate(ccd_df.columns):
        ccd_df[factor] = (ccd_df[factor] + 1) / 2 * (high_values[i] - low_values[i]) + low_values[i]

    ccd_df["DMA"] = 700

    # Initialise Experience No List
    exp_number = []

    # Create the List
    for i in range(len(ccd_df.index)):
        exp_number.append(i + 1)

    # Add the list in the Matrix
    ccd_df['Exp No'] = exp_number

    # Reorder columns
    ccd_df = ccd_df.reindex(
        columns=['Exp No', "Catalyst", "Pyridine", "Substrate", 'DMA'])

    return(ccd_df, ccd_df_skeleton)

CCO_design_RSO = createCCO()[0]
CCO_design_RSO_skeleton = createCCO()[1]