#Summary Assertion
#Summary of accidents casued by drivers without valid driving license. 
import pandas as pd
df = pd.read_csv('Participantonly.csv')
df = df.iloc[:,[7]]
valid_drvr_sts=[1,2]

df = df.dropna(subset=['Driver License Status'])
print(df)
num_rows = df.shape[0]
mask = ~df['Driver License Status'].isin(valid_drvr_sts)
count = mask.sum()

print(f"Number of records for which the column value is not in the array: {count} out of total records: {num_rows}")
