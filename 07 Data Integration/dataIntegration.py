import pandas as pd
import datetime

# Path to the CSV file
COVID_county_data = 'COVID_county_data.csv'

# Read the CSV file and create a DataFrame
df_COVID_county_data = pd.read_csv(COVID_county_data)
# date      county       state     fips  cases  deaths
# Print the DataFrame
#print(df_COVID_county_data['county'])

census_data = 'acs2017_census_tract_data.csv'

df_census_Data= pd.read_csv(census_data, usecols=['County','State','TotalPop','Poverty','IncomePerCap'])

cddf1=df_census_Data.groupby(['County','State']).agg({
    'TotalPop': 'sum',
    'Poverty': 'mean',
    'IncomePerCap':'mean'
}).reset_index()

#Part A
filtered_df = cddf1[(cddf1['State']  == 'Oregon') & (cddf1['County'] == 'Malheur County')]


max_pop_row = cddf1.loc[cddf1['TotalPop'].idxmax()]
min_pop_row = cddf1.loc[cddf1['TotalPop'].idxmin()]

cddf1['ID'] = cddf1.groupby(['State', 'County']).ngroup()
cddf1['County'] = cddf1['County'].str.replace(' County', '', case=False)

# Convert date_column to datetime format
df_COVID_county_data['date'] = pd.to_datetime(df_COVID_county_data['date'])
df_COVID_county_data['month'] = df_COVID_county_data['date'].dt.month
df_COVID_county_data['year'] = df_COVID_county_data['date'].dt.year
df_COVID_county_data = df_COVID_county_data.rename(columns={'county': 'County','state':'State'})

aggregated_county_data = df_COVID_county_data.groupby(['month','year','County','State']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

df_county_ID = pd.merge(cddf1[['ID', 'County','State']], aggregated_county_data, on=['State', 'County'],how='inner')

#Part B
county_id = cddf1.loc[cddf1['County'] == 'Malheur', 'ID'].values[0]
month_number = datetime.datetime.strptime('February'.capitalize(), "%B").month
filtered_county_df = df_county_ID[ (df_county_ID['ID']  == county_id) & (df_county_ID['month'] == month_number)& (df_county_ID['year'] == 2021)]
print(filtered_county_df)

#part c
#print(df_county_ID)

countyData=df_county_ID.groupby(['ID']).agg({
    'cases':'sum',
    'deaths':'sum'
}).reset_index()
#print("=================================")
#print(cddf1)
COVID_summary =pd.merge(countyData, cddf1[['ID','TotalPop','Poverty','IncomePerCap']], on='ID')

county_id = cddf1.loc[(cddf1['State'] == 'Kentucky') & (cddf1['County'] == 'Harlan'), 'ID'].values[0]

#print(county_id)

COVID_summary['TotalCasesPer100K']=COVID_summary['cases']/ (COVID_summary['TotalPop'] /100000)
COVID_summary['TotalCasesPer100K']=COVID_summary['TotalCasesPer100K'].round(2)
COVID_summary['TotalDeathsPer100K']=COVID_summary['deaths']/ (COVID_summary['TotalPop'] /100000)
COVID_summary['TotalDeathsPer100K']=COVID_summary['TotalDeathsPer100K'].round(2)
filtered_summary=COVID_summary[ (COVID_summary['ID']  == county_id)]

#print(filtered_summary)

#part D
oregon_ids=cddf1.loc[(cddf1['State'] == 'Oregon') , 'ID']
oregon_df= COVID_summary[COVID_summary['ID'].isin(oregon_ids)]
print(oregon_df)
R1 = oregon_df['TotalCasesPer100K'].corr(oregon_df['Poverty'])
R2 = oregon_df['TotalDeathsPer100K'].corr(oregon_df['Poverty'])
R3= oregon_df['TotalCasesPer100K'].corr(oregon_df['IncomePerCap'])
R4 = oregon_df['TotalDeathsPer100K'].corr(oregon_df['IncomePerCap'])
R5 = COVID_summary['TotalCasesPer100K'].corr(COVID_summary['Poverty'])
R6 = COVID_summary['TotalDeathsPer100K'].corr(COVID_summary['Poverty'])
R7= COVID_summary['TotalCasesPer100K'].corr(COVID_summary['IncomePerCap'])
R8 = COVID_summary['TotalDeathsPer100K'].corr(COVID_summary['IncomePerCap'])
print(R5)
print(R6)
print(R7)
print(R8)



