#Existence assertions
#For every crash there should be at least one vehicle involved

import pandas as pd
df = pd.read_csv('Vehicleonly.csv')
df = df.iloc[:,[0,1]]

grouped = df.groupby('Crash ID')
for name, group in grouped:
    if group.empty:
        print(f"Crash ID '{name}' does not have vehicles associated with it.")
    else:
        print(f"Crash ID '{name}' has {len(group)} vehicles associated with it.")
