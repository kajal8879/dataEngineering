import pandas as pd
import numpy as np
import matplotlib.pyplot as mplot
import seaborn as sea
from pylab import rcParams
from urllib.request import urlopen
from bs4 import BeautifulSoup

# database sample 1
url = "http://www.hubertiming.com/results/2017GPTR10K"
# database sample 2
# url = "https://www.hubertiming.com/results/2023WyEasterLong"
html = urlopen(url)

#to extract data from the html format
soup = BeautifulSoup(html, 'lxml')
# extract all rows
rows = soup.find_all('tr')

# empty array for result
resultArray = []

# convert html values to string values
for row in rows:
    td = row.find_all("td")
    text = str(td)
    Ftext = BeautifulSoup(text, 'lxml').get_text()
    resultArray.append(Ftext)

# converting the result in to dataframe
df = pd.DataFrame(resultArray)

# splitting the columns
df1 = df[0].str.split(',', expand=True)

# extract table headers
headers = soup.find_all("th")

# empty array for result
headerArray = []
headerText = str(headers)
header = BeautifulSoup(headerText, 'lxml').get_text()
headerArray.append(header)

# dataframe for header
df2 = pd.DataFrame(headerArray)

# splitting the header
df3 = df2[0].str.split(',', expand=True)
df3 = df3.apply(lambda x: x.str.strip('[]'))

combinedHeaderRows = [df3, df1]
df4 = pd.concat(combinedHeaderRows)

df4 = df4.apply(lambda x: x.str.strip('[]'))
df5 = df4.dropna(axis=0, how='any')
df6 = df5.rename(columns=df5.iloc[0])
df7 = df6.drop(df6.index[0])

# removing \r \n characters from data frame
df7 = df7.replace(r'\n', ' ', regex=True)
df7 = df7.replace(r'\r', ' ', regex=True)
df7 = df7.replace(r'  ', '', regex=True)

# visualization part
time_list = df7[' Time'].tolist()

# empty array
time_mins = []

# converting time in to mins
def hms_to_s(time):
    t = 0
    for u in time.split(':'):
        t = 60 * t + int(u)
    return t / 60


for t in time_list:
    time_mins.append(hms_to_s(t))

# New column to the data frame
df7['Runner_mins'] = time_mins
print(df7)

# visualization using pylab
# finish time of player visualization
rcParams['figure.figsize'] = 12, 5
df7.boxplot(column='Runner_mins')
mplot.grid(True, axis='y')
mplot.ylabel(' Time')
mplot.xticks([1], ['Runners'])
mplot.show()

# normal distribution for player finish time
plot = df7['Runner_mins']
sea.displot(plot, kde=True)
mplot.show()

#  performance differences between males and females of various age groups
f = df7.loc[df7[' Gender'] == ' F']['Runner_mins']
m = df7.loc[df7[' Gender'] == ' M']['Runner_mins']
sea.histplot(f, kde=True, label='Female')
sea.histplot(m, kde=True, color='red', fill=False, linewidth=0)
sea.kdeplot(m, color='red', label='Male')
mplot.title('Performance')
mplot.legend()
mplot.show()

# Groupby Statistics
grouping_stats = df7.groupby(" Gender", as_index=True).describe()
print(grouping_stats)

# Final Visualization
df7.boxplot(column='Runner_mins', by=' Gender')
mplot.ylabel('Chip Time')
mplot.suptitle("")
mplot.show()
# ------------------------------------------------------------------------------------------
