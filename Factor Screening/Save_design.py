# Import Packages
import pandas as pd
import openpyxl

# Import data
#exp_design = pd.DataFrame(SFData)
exp_design = SFData

# Define saving location
saveplace = saveFolder + '/FactorScreening_Design.xlsx'

# Save the Dataframe in an Excel File
exp_design.to_excel(saveplace, index=False, sheet_name="Factor Screening Design")