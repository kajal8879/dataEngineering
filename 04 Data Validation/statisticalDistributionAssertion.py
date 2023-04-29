#Statistical Distribution Assertion
#The number of persons involved in the crash will be same as  Total Pedestrian Count + Total Pedalcyclist Count + 
# Total Unknown Count + Total Occupant Count.

import pandas as pd
df = pd.read_csv('Crashonly.csv')
df = df.iloc[:,[0,61,62]]
num_rows = df.shape[0]
df = df.dropna(subset=['School Zone Indicator','Work Zone Indicator'])
print(df)
totalCrashes = df['Crash ID'].nunique()
schoolZoneCrashes = (df['School Zone Indicator'] == 1).sum()
workZoneCrashes = (df['Work Zone Indicator'] == 1).sum()
print(f"out of {totalCrashes} crashes,  {schoolZoneCrashes} happened in school zone and {workZoneCrashes} happened in work zone")