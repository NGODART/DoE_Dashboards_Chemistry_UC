import numpy as np
import pandas as pd
from pyDOE2 import fracfact

# Define the experimental line order  (Still a hardcoding way to do it, but it reduces code length)
line_order = [1, 6, 12, 15, 3, 8, 10, 13, 4, 7, 9, 14, 2, 5, 11, 16]

# Convert the list to a numpy array of integers
line_order = np.array(line_order, dtype=int)

# Generate the design matrix
design = fracfact("a b c d abcd")

# Reorder the rows of the design matrix according to the experimental line order
design = design[line_order - 1, :]

# Define the number of blocks
num_blocks = 4

# Calculate the number of runs per block
num_runs_per_block = int(len(design) / num_blocks)

# Create an array to store the blocks
blocks = []

# Iterate over each block
for i in range(num_blocks):
    # Extract the runs for the current block
    block_runs = design[i * num_runs_per_block: (i + 1) * num_runs_per_block].copy()

    # Add the center points to the block
    center_points = np.tile([0, 0, 0, 0, 0], (2, 1))
    block_runs = np.concatenate((block_runs, center_points), axis=0)

    # Append the block label to each run in the block
    block_label = f"B{i+1}"
    block_labels = np.full((len(block_runs), 1), block_label)
    block_runs = np.concatenate((block_labels, block_runs), axis=1)

    # Append the block to the list of blocks
    blocks.append(block_runs)

# Concatenate the blocks along the first axis to get the final design matrix
design_with_blocks = np.concatenate(blocks, axis=0)

# Convert the design matrix to a Pandas DataFrame
columns = ["Block", "Temperature", "DMA", "Catalyst", "Pyridine", "Atmosphere"]
df = pd.DataFrame(data=design_with_blocks, columns=columns)

# Type float in the 'Atmosphere' column to replace values by String
df['Atmosphere'] = df['Atmosphere'].astype(float)

# Initialise the Atmosphere List
atmos_str = []

# Browse the dataframe
for index, row in df.iterrows():
    # Check the value of the column Atmosphere_code for this row
    if row['Atmosphere'] == 0 or row['Atmosphere'] == -1:
        atmos_str.append('Argon')
    elif row['Atmosphere'] == 1:
        atmos_str.append('Air')


# Add the list in the Matrix
df['Atmosphere'] = atmos_str

df_skeleton= df.copy()

# Define low and high value for each factor
low_values = [100, 400, 1, 4, 0]
high_values = [140, 1000, 4, 30, 1]

# Redefine factor levels for numerical factors
for i, factor in enumerate(df.columns[1:5]):
    df[factor] = df[factor].astype(float)
    df[factor] = (df[factor] + 1) / 2 * (high_values[i] - low_values[i]) + low_values[i]


# Initialise Experience No List
exp_number = []

# Create the List
for i in range(len(df.index)):
    exp_number.append(i + 1)

# Add the list in the Matrix
df['Exp No'] = exp_number
df_skeleton['Exp No'] = exp_number

# Reorder columns
df = df.reindex(columns=['Exp No', 'Temperature', 'DMA', 'Catalyst', 'Pyridine', 'Atmosphere', 'Block'])
df_skeleton = df_skeleton.reindex(columns=['Exp No', 'Temperature', 'DMA', 'Catalyst', 'Pyridine', 'Atmosphere', 'Block'])

print(df)
print(df_skeleton)