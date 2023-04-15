import requests
from datetime import date

# Give city name
cityInput = input("Enter city name: ")
date_input = input("Enter date for your next class in YYYY-MM-DD format: ")

weatherApi = "https://weatherapi-com.p.rapidapi.com/forecast.json"

headers = {
	"X-RapidAPI-Key": "65c9213e55mshbdd24dff0a55013p19ca0djsn174af0375cd5",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

q1 = {"q":cityInput,"dt":date.today()}
res1 = requests.request("GET", weatherApi, headers=headers, params=q1)
jsonRes1 = res1.json()

if(jsonRes1.get('forecast').get('forecastday')[0].get('day').get('daily_will_it_rain') == 1):
    print("It is raining today in " + cityInput) 
else:
    print("It is not raining today in " + cityInput)

    
q2 = {"q":cityInput,"dt":date_input}
res2 = requests.request("GET", weatherApi, headers=headers, params=q2)
jsonRes2 = res2.json()

if(jsonRes2.get('forecast').get('forecastday')[0].get('day').get('daily_will_it_rain') == 1):
    print("It will rain in " + cityInput +" when we meet for next class ")
else:
    print("It will not rain in " + cityInput + " on " + str(date_input))
