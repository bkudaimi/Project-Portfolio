import requests
'''
This program retrieves and presents weather data from OpenWeatherMap
DSC 510
Final Programming Assignment 10.2
Author: Bilal Kudaimi
August 9, 2020
'''
print('This program retrieves and presents weather data from OpenWeatherMap' '\nDSC 510')
print('Final Programming Assignment 10.2', '\nAuthor: Bilal Kudaimi')
print('August 9, 2020')
print(' ')
print('Welcome, User')


# Requests the weather data
def weather_request(cityNameorZIP):
    # Builds a URL using the API key and the city/ZIP code
    # Uses if statements to ensure a valid city name is entered
    defaultURL = 'http://api.openweathermap.org/data/2.5/weather?'
    APIKey = '323826a899ef543d89a4075aad70c24a'
    url = defaultURL + 'appid={}'.format(APIKey) + "&q={}".format(cityNameorZIP) + '&units=imperial'
    if cityNameorZIP.isnumeric() == True and len(cityNameorZIP) == 5:
        url = defaultURL + 'appid=' + APIKey + "&zip=" + cityNameorZIP + '&units=imperial'

    # Retrieves weather data
    # Returns an error message if no connection is made or invalid data is entered
    try:
        response = requests.get(url)
        organizedData = response.json()
        if organizedData['cod'] == '404':
            print('\nInvalid city name or ZIP code entered.')
        else:
            print('\nConnected to the service', '\n ')
            return organizedData
    except:
        print('\nCould not connect to the service')

# Prints the weather data in a readable format
# Will return an error if the data could not be retrieved
def weather_pretty_print(organizedData):
    try:
    # Pulling the weather data from the dictionary
        weatherData = organizedData['main']

    # Separating out the temperature, pressure, humidity, and weather report
        temperature = weatherData['temp']
        minTemp = weatherData['temp_min']
        maxTemp = weatherData['temp_max']
        pressure = weatherData['pressure']
        humidity = weatherData['humidity']
        report = organizedData['weather']

    # Displaying the separated weather data
        print('{}, {}'.format(organizedData['name'], organizedData['sys']['country']))
        print('Temperature: {:.2f} F'.format(temperature))
        print('Low: {} F'.format(minTemp))
        print('High: {} F'.format(maxTemp))
        print('Pressure: {} inHg'.format(pressure * 0.03))
        print('Humidity: {} %'.format(humidity))
        print('Weather Report: {}'.format(report[0]['description']))
    except:
        print('\nCould not retrieve data.')

# Main function
def main():
    while True:
        cityNameorZIP = input('Enter the city name or 5-digit ZIP code you would like the weather for. '
                              '\nUse the following format: CITY, STATE, US (ex: Stillwater, MN, US for Minnesota)'
                              '\nFor cities outside the US, enter the city name followed by the country identifier 3(ex: Tokyo, JP for Japan): ')
        if cityNameorZIP == '':
            print('Nothing was entered')
            continue
        x = weather_request(cityNameorZIP)
        weather_pretty_print(x)
        loopDecider = input('Would you like to get weather data for another city/ZIP? (Y/N): ')
        if loopDecider.upper() == 'Y':
            print(' ')
            continue
        elif loopDecider.upper() == 'N':
            input('Thank you for using this weather app. Press enter to exit.')
            break

if __name__ == "__main__":
    main()