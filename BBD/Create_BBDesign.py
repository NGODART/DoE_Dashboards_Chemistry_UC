# Import packages
import pandas as pd
from pyDOE2 import bbdesign

def createBBD():

        # Define the number of factors and their ranges
        factors = ["Catalyst", "Pyridine", "Substrate"]
        low_values = [1, 5, 5]
        high_values = [4, 30, 25]

        # Generate the central composite design matrix
        bbd_matrix = bbdesign(len(factors), center=3)

        # Convert the design matrix to a Pandas DataFrame
        bbd_df = pd.DataFrame(bbd_matrix, columns=factors)

        # Apply real levels 
        for i, factor in enumerate(bbd_df.columns):
                bbd_df[factor] = (bbd_df[factor] + 1) / 2 * (high_values[i] - low_values[i]) + low_values[i]

        bbd_df["DMA"] = 700

        # Initialise Experience No List
        exp_number = []

        # Create the List
        for i in range(len(bbd_df.index)):
                exp_number.append(i + 1)

        # Add the list in the Matrix
        bbd_df['Exp No'] = exp_number

        # Reorder columns
        bbd_df = bbd_df.reindex(columns=['Exp No', "Catalyst", "Pyridine", "Substrate", 'DMA'])

        return(bbd_df)

DDB_RSO = createBBD()