# Import Packages
import pandas as pd
import openpyxl

# Import data
exp_design = SFData

# import saving place
saveplace = saveFolder + '/RSO_BB_Design.xlsx'

# Save the Dataframe in an Excel File
exp_design.to_excel(saveplace, index=False, sheet_name="BB Design")