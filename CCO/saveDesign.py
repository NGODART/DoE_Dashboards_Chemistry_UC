# Import packages
import pandas as pd
import openpyxl

# Import data
exp_design = SFData

# Import saving folder
saveplace = saveFolder + '/RSO_CCO_Design.xlsx'

# Save the Dataframe in an Excel File
exp_design.to_excel(saveplace, index=False, sheet_name="CCO Design")