#limit assertions
#Latitude degrees should be between 41 to 47 inclusive
import pandas as pd
df = pd.read_csv('Crashonly.csv')
df = df.iloc[:,[19]]

df = df.dropna(subset=['Latitude Degrees'])
# Check if all the values in a column fall under a certain range
if ((df['Latitude Degrees'] >= 41) & (df['Latitude Degrees'] <= 47)).all():
    print("Latitude Degrees comees between 41 to 47 (inclusive)")
else:
    print("Not all values in the column Latitude Degrees comees between 41 to 47 (inclusive)")

