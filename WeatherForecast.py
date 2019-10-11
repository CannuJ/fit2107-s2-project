"""
Weather Forecast Program

API Key - 404db912ca95cf6ac23f4362c048124f
"""

from optparse import OptionParser
import json
import requests

def jprint(obj):
    # Creates a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print("\n"+text+"\n")

def main():

    api_default = "404db912ca95cf6ac23f4362c048124f"

    parser = OptionParser()

    parser.set_defaults(api=api_default, city="Melbourne,AU", temp='metric')
    parser.add_option('--api', action='store', dest='api', help='Specify API Key used to connect to OpenWeatherMap.')
    parser.add_option('--city', action='store', dest='city', help='Specify City you would like to check weather of.')
    parser.add_option('--cid', action='store', dest='cid', help='Specify CityID you would like to check weather of.')
    parser.add_option('--gc', action='store', dest='gc', help='Geographic Coordinates for where to to check weather.')
    parser.add_option('-z', action='store', dest='z', help='Specify ZipCode for where you would like to check weather.')
    parser.add_option('--time', action='store_const', const='time', dest='time', help='Displays date/time.')
    parser.add_option('--temp', action='store', dest='temp', help='Specify units for temperature (Celsius/Fahrenheit.')
    parser.add_option('--pressure', action='store_const', const='pressure', dest='pressure', help='Displays pressure.')
    parser.add_option('--cloud', action='store_const', const='cloud', dest='cloud', help='Displays cloud type.')
    parser.add_option('--humidity', action='store_const', const='humidity', dest='humidity', help='Displays humidity.')
    parser.add_option('--wind', action='store_const', const='wind', dest='wind', help='Displays wind information.')
    parser.add_option('--sunset', action='store_const', const='sunset', dest='sunset', help='Displays sunset time.')
    parser.add_option('--sunrise', action='store_const', const='sunrise', dest='sunrise', help='Displays sunrise time.')

    # Testing Argument for Dumping Entire Response from OpenWeatherMap
    parser.add_option('--debug', action='store_const', const='debug', dest='debug', help='Dumps entire response.')

    (options, args) = parser.parse_args()

    parameters = {
        "APPID": options.api,
        "q" : options.city,
        "units" : options.temp,
    }

    request_url = "http://api.openweathermap.org/data/2.5/weather?"

    response = requests.get(request_url, params=parameters)

    print("\nResponse Code = " + str(response.status_code))

    if options.debug:
        print("Parameters: " + str(options)) # Parameters Inputted by User
        jprint(response.json()) # Dump Full Output from OpenWeatherMap

    location = str(response.json()['name']) + ", " + str(response.json()['sys']['country'])

    temp_min = str(response.json()['main']['temp_min'])
    temp_max = str(response.json()['main']['temp_max'])

    print("\nThe temperature in " + location + " ranges from "+ temp_min +" - "+temp_max+" celsius.\n")

if __name__=="__main__":
    main()

