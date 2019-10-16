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

    # Check exactly one of [api, city, cid, gc] have been supplied, else return error message.
    if location_inputs == 0:
        print("\nYou have not supplied a location. Please use only one of [city, cid, gc, z].\n")
        return False
    if location_inputs > 1:
        print("\nMultiple chosen locations are specified. Please use only one of [city, cid, gc, z].\n")
        return False

    return True

def get_response(options):
    # Prepare parameters that are sent to API

    # Parameter only takes "Metric" and "Imperial". Correct accordingly
    if options.temp == "Celsius":
        options.temp = "Metric"
    if options.temp == "Fahrenheit":
        options.temp = "Imperial"

    if options.temp != "Metric" or "Imperial":
        print("Woah slow down there sonny!")
        print("Temperatures outputting in Kelvin (K)")

    if options.gc:

        try:
            parameters = {
                "APPID": options.api,
                "q": options.city,
                "id": options.cid,
                "lat": options.gc.split()[0],
                "lon": options.gc.split()[1],
                "zip": options.z,
                "units": options.temp,
            }
        except:
            print("\nIncorrect format for Geographic Coordinates. Usage: --gc \"Latitude Longitude\"\n")
            exit(1)

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

    if str(response.status_code) == "400":
        print("\nError 400 - " + str(response.json()['message']) + "\n")
        return False

    if str(response.status_code) == "401":
        print("\nInvalid API Key Supplied. Please see http://openweathermap.org/faq#error401 for more info.\n")
        return False

    if str(response.status_code) == "404":
        print("\nError 404 - " + str(response.json()['message']) + "\n")
        return False

    if str(response.status_code) == "429":
        print("\nError 429 - " + str(response.json()['message']) + "\n")
        return False

    return True

def debug(response, options):
    print("\nResponse Code = " + str(response.status_code))
    print("\nOptions: " + str(options))  # Options Inputted by User (Both API and Non-Api)
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
        time_stamp = datetime.utcfromtimestamp(int(response.json()['dt'])+
                                            int(response.json()['timezone'])).strftime('%Y-%m-%d %H:%M:%S')
        time_offset = str(int(response.json()['timezone']) // 3600)

        if (0 < int(time_offset)) and (int(time_offset) < 10):
            time_offset = "+0" + str(time_offset)
        elif int(time_offset) >= 10:

            time_offset = "+" + str(time_offset)
        elif int(time_offset) > -10:
            time_offset = str(time_offset[0]) + "0" + str(time_offset[1])
        else:
            time_offset = str(time_offset)

        output_string += "On " + str(time_stamp) + str(time_offset) + \
                         ", the temperature in [" + location + "] ranges from "
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
        try:
            wind_speed = str(response.json()['wind']['speed'])
            wind_deg = str(response.json()['wind']['deg']) # May not always output

            # Wind Speed is given in m/s for Metric, miles/hr for Imperial
            if options.temp == "Imperial":
                output_string += " Wind is blowing at " + wind_speed + " miles/hr from " + wind_deg + " degrees."
            else:
                output_string += " Wind is blowing at " + wind_speed + " metres/s from " + wind_deg + " degrees."

        except:
            wind_speed = str(response.json()['wind']['speed'])

            # Wind Speed is given in m/s for Metric, miles/hr for Imperial
            if options.temp == "Imperial":
                output_string += " Wind is blowing at " + wind_speed + " miles/hr."
            else:
                output_string += " Wind is blowing at " + wind_speed + " metres/s."

    # Sunrise, Sunset

    if options.sunrise and options.sunset:
        sunrise = datetime.utcfromtimestamp(int(response.json()['sys']['sunrise']) +
                                            int(response.json()['timezone'])).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(int(response.json()['sys']['sunset']) +
                                            int(response.json()['timezone'])).strftime('%H:%M:%S')
        time_offset = str(int(response.json()['timezone'])//3600)

        if int(time_offset) > 0 < 10:
            time_offset = "+0" + str(time_offset)
        elif int(time_offset) >= 10:
            time_offset = "+" + str(time_offset)
        elif int(time_offset) > -10:
            time_offset = str(time_offset[0]) + "0" +  str(time_offset[1])
        else:
            time_offset = str(time_offset)

        output_string += " Sunrise is at " + str(sunrise) + str(time_offset) + ", and Sunset is at " \
                         + str(sunset) + str(time_offset) + "."

    elif options.sunrise:
        sunrise = datetime.utcfromtimestamp(int(response.json()['sys']['sunrise']) +
                                            int(response.json()['timezone'])).strftime('%H:%M:%S')
        time_offset = str(int(response.json()['timezone'])//3600)

        if int(time_offset) > 0 < 10:
            time_offset = "+0" + str(time_offset)
        elif int(time_offset) >= 10:
            time_offset = "+" + str(time_offset)
        elif int(time_offset) > -10:
            time_offset = str(time_offset[0]) + "0" + str(time_offset[1])
        else:
            time_offset = str(time_offset)

        output_string += " Sunrise is at " + str(sunrise) + str(time_offset) + "."

    elif options.sunset:
        sunset = datetime.utcfromtimestamp(int(response.json()['sys']['sunset']) +
                                            int(response.json()['timezone'])).strftime('%H:%M:%S')
        time_offset = str(int(response.json()['timezone'])//3600)

        if int(time_offset) > 0 < 10:
            time_offset = "+0" + str(time_offset)
        elif int(time_offset) >= 10:
            time_offset = "+" + str(time_offset)
        elif int(time_offset) > -10:
            time_offset = str(time_offset[0]) + "0" + str(time_offset[1])
        else:
            time_offset = str(time_offset)

        output_string += " Sunset is at " + str(sunset) + str(time_offset) + "."

    print(output_string + "\n")


def main():
    parser = weather_args()
    (options,args) = parser.parse_args(sys.argv[1:])

    if not check_num_of_location_input(options):
        exit(1)

    response = get_response(options)

    if not check_response(response):
        exit(1)

    # Debug Conditional
    if options.debug:
        debug(response, options)

    # Print city information
    try:
        location = str(response.json()['name']) + ", " + str(response.json()['sys']['country'])
    except KeyError:
        location = str(response.json()['coord']['lat']) + ", " + str(response.json()['coord']['lon']) + " (Coordinates)"

    # Print all the requested information by user
    print_info(options,response,location)


if __name__ == "__main__":
    main()
