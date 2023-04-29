#Inter-Record Assertion
#The "Crash ID" field for each record should be unique and non-empty.

import pandas as pd
df = pd.read_csv('Crashonly.csv')
df = df.iloc[:,[0]]
if df['Crash ID'].notnull().all() :
    print("The 'Crash ID' column has all non-empty")
else:
    print("The 'Crash ID' column does not have all non-empty ")
