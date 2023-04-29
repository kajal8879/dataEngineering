#Intra Record Assertion
#Latitude Minutes must be “null” when Latitude Degrees is “null”
import pandas as pd
df = pd.read_csv('Crashonly.csv')
df = df.iloc[:,[19,20]]

df = df.dropna(subset=['Latitude Degrees','Latitude Minutes'])
print(df)
df = df.dropna(subset=['Latitude Degrees'], inplace=True)
if df.isnull().any().any():
    print("Latitude Minutes is “null” when Latitude Degrees is “null”")
else:
    print("Latitude Minutes is not “null” when Latitude Degrees is “null”")
