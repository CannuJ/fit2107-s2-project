"""
Weather Forecast Program

API Key - 404db912ca95cf6ac23f4362c048124f
"""

from datetime import datetime
from optparse import OptionParser
import json
import requests
import sys

def jprint(obj):

    # Creates a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print("\n"+text+"\n")

def weather_args():
    parser = OptionParser()

    api_default = "404db912ca95cf6ac23f4362c048124f"

    parser.set_defaults(api=api_default, temp='Metric')
    parser.add_option('--api', action='store', dest='api', help='Specify API Key used to connect to OpenWeatherMap.')
    parser.add_option('--city', action='store', dest='city', help='Specify City you would like to check weather of.')
    parser.add_option('--cid', action='store', dest='cid', help='Specify CityID you would like to check weather of.')
    parser.add_option('--gc', action='store', dest='gc', help='Geographic Coordinates "Latitude Longitude".')
    parser.add_option('-z', action='store', dest='z', help='Specify ZipCode for where you would like to check weather.')
    parser.add_option('--time', action='store_const', const='time', dest='time', help='Displays date/time.')
    parser.add_option('--temp', action='store', dest='temp', help='Specify units for temperature (Celsius/Fahrenheit.')
    parser.add_option('--pressure', action='store_const', const='pressure', dest='pressure', help='Displays pressure.')
    parser.add_option('--cloud', action='store_const', const='cloud', dest='cloud', help='Displays cloud type.')
    parser.add_option('--humidity', action='store_const', const='humidity', dest='humidity', help='Displays humidity.')
    parser.add_option('--wind', action='store_const', const='wind', dest='wind', help='Displays wind information.')
    parser.add_option('--sunset', action='store_const', const='sunset', dest='sunset', help='Displays sunset time.')
    parser.add_option('--sunrise', action='store_const', const='sunrise', dest='sunrise', help='Displays sunrise time.')

    # Testing Argument for Dumping Entire Response from OpenWeatherMap as well as Parameters sent to API.
    parser.add_option('--debug', action='store_const', const='debug', dest='debug', help='Dumps entire response.')

    return parser

def check_num_of_location_input(options):
    # Count Location Inputs

    location_inputs = 0
    if options.city:
        location_inputs += 1
    if options.cid:
        location_inputs += 1
    if options.gc:
        location_inputs += 1
    if options.z:
        location_inputs += 1

    return location_inputs

def get_response(options):
    # Prepare parameters that are sent to API

    if options.gc:

        parameters = {
            "APPID": options.api,
            "q": options.city,
            "id": options.cid,
            "lat": options.gc.split()[0],
            "lon": options.gc.split()[1],
            "zip": options.z,
            "units": options.temp,
        }

    else:
        parameters = {
            "APPID": options.api,
            "q": options.city,
            "id": options.cid,
            "zip": options.z,
            "units": options.temp,
        }

    request_url = "http://api.openweathermap.org/data/2.5/weather?"
    response = requests.get(request_url, params=parameters)
    return response

def check_response(response):
    # Check if response was valid

    if str(response.status_code) == "401":
        print("\nInvalid API Key Supplied. Please see http://openweathermap.org/faq#error401 for more info.\n")
        exit(1)

    if str(response.status_code) == "404":
        print("\nError 404 - " + str(response.json()['message']) + "\n")
        exit(1)

def debug(response):
    print("\nResponse Code = " + str(response.status_code))
    print("\nParameters: " + str(options))  # Parameters Inputted by User
    print("\nSee full json response below:")
    jprint(response.json())  # Dump Full Output from OpenWeatherMap
    print("\nActual Output:")

def print_info(options,response,location):

    # Temperature
    temp_min = str(response.json()['main']['temp_min'])
    temp_max = str(response.json()['main']['temp_max'])

    # Conditional Outputs depending on non-api parameters

    output_string = "\n"  # Build string depending on parameters

    # Time Output

    if options.time:
        time_stamp = datetime.utcfromtimestamp(int(response.json()['dt'])).strftime('%Y-%m-%d %H:%M:%S+00')
        output_string += "On " + str(time_stamp) + "+00, the temperature in [" + location + "] ranges from "
    else:
        output_string += "The temperature in [" + location + "] ranges from "

    # Temperature Units

    if options.temp == "Imperial":
        output_string += temp_min + " - " + temp_max + " Fahrenheit."
    else:
        output_string += temp_min + " - " + temp_max + " Celsius."

    # Pressure

    if options.pressure:
        pressure = str(response.json()['main']['pressure'])
        output_string += " Atmospheric Pressure is at " + pressure + "hPa."

    # Cloud

    if options.cloud:

        found_cloudy = False

        # If cloud data is contained in response, offer extended output
        for i in range(len(response.json()['weather'])):
            if "Clouds" in str(response.json()['weather'][i]['main']):
                found_cloudy = True
                cloud_desc = str(response.json()['weather'][i]['description'])
                cloud = str(response.json()['clouds']['all'])
                output_string += " Seeing " + cloud_desc + " with about " + cloud + "% coverage."

        if not found_cloudy:
            cloud = str(response.json()['clouds']['all'])
            output_string += " Cloud Density is " + cloud + "%."

    # Humidity

    if options.humidity:
        humidity = str(response.json()['main']['humidity'])
        output_string += " Humidity is " + humidity + "%."

    # Wind

    if options.wind:
        wind_speed = str(response.json()['wind']['speed'])
        wind_deg = str(response.json()['wind']['deg'])

        # Wind Speed is given in m/s for Metric, miles/hr for Imperial
        if options.temp == "Imperial":
            output_string += " Wind is blowing at " + wind_speed + " miles/hr from " + wind_deg + " degrees."
        else:
            output_string += " Wind is blowing at " + wind_speed + " metres/s from " + wind_deg + " degrees."

    # Sunrise, Sunset
    # TODO: Convert to Local Timezone??

    if options.sunrise and options.sunset:
        sunrise = datetime.utcfromtimestamp(int(response.json()['sys']['sunrise'])).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(int(response.json()['sys']['sunset'])).strftime('%H:%M:%S')
        output_string += " Sunrise is at " + str(sunrise) + "+00 , and Sunset is at " + str(sunset) + "+00."

    elif options.sunrise:
        sunrise = datetime.utcfromtimestamp(int(response.json()['sys']['sunrise'])).strftime('%H:%M:%S')
        output_string += " Sunrise is at " + str(sunrise) + "+00."

    elif options.sunset:
        sunset = datetime.utcfromtimestamp(int(response.json()['sys']['sunset'])).strftime('%H:%M:%S')
        output_string += " Sunset is at " + str(sunset) + "+00."

    print(output_string + "\n")


def main():
    parser = weather_args()
    (options,args) = parser.parse_args(sys.argv[1:])


    location_inputs = check_num_of_location_input(options)
    # Check exactly one of [api, city, cid, gc] have been supplied, else return error message.
    if location_inputs == 0:
        print("\nYou have not supplied a location. Please use only one of [city, cid, gc, z].\n")
        exit(1)
    if location_inputs > 1:
        print("\nMultiple chosen locations are specified. Please use only one of [city, cid, gc, z].\n")
        exit(1)

    # Parameter only takes "Metric" and "Imperial". Correct accordingly
    if options.temp == "Celsius":
        options.temp = "Metric"
    if options.temp == "Fahrenheit":
        options.temp = "Imperial"

    response = get_response(options)

    check_response(response)

    # Debug Conditional
    if options.debug:
        debug(response)

    # Print city information
    try:
        location = str(response.json()['name']) + ", " + str(response.json()['sys']['country'])
    except KeyError:
        location = str(response.json()['coord']['lat']) + ", " + str(response.json()['coord']['lon']) + " (Coordinates)"

    # Print all the requested information by user
    print_info(options,response,location)


if __name__ == "__main__":
    main()
