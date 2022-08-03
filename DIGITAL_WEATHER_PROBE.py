import urllib, json, requests, csv
from datetime import datetime
from time import sleep
from timeit import default_timer as timer

# NWS API
# Code in this section pulls data from the NWS API

# Access Natioal Weather Service API
# Loads NWS site that corresponds to a lattitude + longitude
# This page contains a link to a JSON with forecast data
# Use getForecast() to open the forecast page
def getPoint(lat, long):
	url = "https://api.weather.gov/points/" + lat + "," + long
	response = urllib.request.urlopen(url)
	pointJSON = json.loads(response.read())	
	return getForecast(pointJSON['properties']['forecast']) #TODO Convert to hourly forecast

# Access NWS forecast data
def getForecast(url):
	response = urllib.request.urlopen(url)
	forecastJSON = json.loads(response.read())
	return forecastJSON

def display(forecastJSON):
	print(forecastJSON['properties']['periods'][0]['name'] + " will be " + str(forecastJSON['properties']['periods'][0]['temperature']) + " F, with " + forecastJSON['properties']['periods'][0]['windDirection'] + " wind " + forecastJSON['properties']['periods'][0]['windSpeed'] + ". " + forecastJSON['properties']['periods'][0]['shortForecast'] + ".")

# Record forecast data in a CSV file
def recordData(forecastJSON):
	wndSpd = forecastJSON['properties']['periods'][0]['windSpeed'][:2]
	fields = [forecastJSON['properties']['periods'][0]['temperature'],forecastJSON['properties']['periods'][0]['windDirection'],wndSpd,forecastJSON['properties']['periods'][0]['shortForecast']]
	with open('data.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow(fields)

# Introduces program and gathers user lat/long data.
# TODO Implement a way to save user lat/long from past sessions
def startup():
	print("Hello and welcome to Digital Weather Probe. \nThis probe tracks weather forecast data for any location in the United States. \nWhere in the United States are you tuning in from?\n")
	print("Please enter your latitude:")
	lat = input()
	print("Please enter your longitude:")
	long = input()
	print("Thank you. Fetching your local weather report now", end='')
	sleep(0.66)
	print(".", end='')
	sleep(0.66)
	print(".", end='')
	sleep(0.66)
	print(".\n")

	forecastJSON = getPoint(lat, long)
	start = timer()

	while (True): #TODO Add exit key
		display(forecastJSON)
		recordData(forecastJSON)

		now = datetime.now()
		dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
		print("\nData recorded succesfully at ", dt_string)

		end = timer()
		elapsedTime = int(end - start)
		print("Total run time of probe: " + '{:02}:{:02}:{:02}'.format(elapsedTime//3600, elapsedTime%3600//60, elapsedTime%60))

		print("--------------------")

		for x in range(6):
			sleep(3600)
			print("Total run time of probe: " + '{:02}:{:02}:{:02}'.format(elapsedTime//3600, elapsedTime%3600//60, elapsedTime%60))
		
startup()
