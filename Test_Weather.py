import unittest
from unittest.mock import Mock
from optparse import OptionParser
from WeatherForecast import *
from unittest.mock import patch
import sys
import responses


class parser_test(unittest.TestCase):
    def setUp(self):
        self.parser = weather_args()

    def test_api(self):
        (options,args) = self.parser.parse_args(['--api=key'])
        self.assertEqual(options.api,'key')

    def test_city(self):
        (option,self.parser) = self.parser.parse_args(["--city=CITY"])
        self.assertTrue(option.city)

    def test_cid(self):
        (option, self.parser) = self.parser.parse_args(["--cid=code"])
        self.assertTrue(option.cid)

    def test_gc(self):
        (option, self.parser) = self.parser.parse_args(['--gc="10 10"'])
        self.assertTrue(option.gc)

    def test_z(self):
        (option, self.parser) = self.parser.parse_args(['-z=zipcode'])
        self.assertTrue(option.z)

    def test_time(self):
        (option, self.parser) = self.parser.parse_args(['--time'])
        self.assertTrue(option.time)

    def test_temp(self):
        (option, self.parser) = self.parser.parse_args(['--temp==Celsius'])
        self.assertTrue(option.temp)

    def test_pressure(self):
        (option, self.parser) = self.parser.parse_args(['--pressure'])
        self.assertTrue(option.pressure)

    def test_cloud(self):
        (option, self.parser) = self.parser.parse_args(['--cloud'])
        self.assertTrue(option.cloud)

    def test_humidity(self):
        (option, self.parser) = self.parser.parse_args(['--humidity'])
        self.assertTrue(option.humidity)

    def test_wind(self):
        (option, self.parser) = self.parser.parse_args(['--wind'])
        self.assertTrue(option.wind)

    def test_sunset(self):
        (option, self.parser) = self.parser.parse_args(['--sunset'])
        self.assertTrue(option.sunset)

    def test_sunrise(self):
        (option, self.parser) = self.parser.parse_args(['--sunrise'])
        self.assertTrue(option.sunrise)

    def test_debug(self):
        (option, self.parser) = self.parser.parse_args(['--debug'])
        self.assertTrue(option.debug)

    def test_invalid(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['--k'])


class check_num_of_location_input_test(unittest.TestCase):
    def setUp(self):
        self.parser = weather_args()

    def test_city_only(self):
        (option, self.parser) = self.parser.parse_args(["--city=CITY"])
        self.assertTrue(check_num_of_location_input(option))

    def test_cid_only(self):
        (option, self.parser) = self.parser.parse_args(["--cid=code"])
        self.assertTrue(check_num_of_location_input(option))

    def test_gc_only(self):
        (option, self.parser) = self.parser.parse_args(['--gc=[23.01.0 113.07.0]'])
        self.assertTrue(check_num_of_location_input(option))

    def test_z_only(self):
        (option, self.parser) = self.parser.parse_args(['-z=zipcode'])
        self.assertTrue(check_num_of_location_input(option))

    def test_no__location_input(self):
        (option, self.parser) = self.parser.parse_args(["--api=API"])
        self.assertFalse(check_num_of_location_input(option))

    def test_combination(self):
        (option, self.parser) = self.parser.parse_args(["--city=CITY", "--cid=CityID"])
        self.assertFalse(check_num_of_location_input(option))

class get_response_test(unittest.TestCase):
    def setUp(self):
        self.parser = weather_args()

    def test_metric_gc(self):
        (option, self.parser) = self.parser.parse_args(["--temp=Celsius", "--gc=-37.81 144.96"])
        self.assertTrue(check_response(get_response(option)))

    def test_imperial_gc(self):
        (option, self.parser) = self.parser.parse_args(["--temp=Fahrenheit", "--gc=-37.81 144.96"])
        self.assertTrue(check_response(get_response(option)))

    def test_valid_city(self):
        (option, self.parser) = self.parser.parse_args(["--city=Melbourne"])
        self.assertTrue(check_response(get_response(option)))

    def test_invalid_temp(self):
        (option, self.parser) = self.parser.parse_args(["--temp=Kelvin", "--gc=-37.81 144.96"])
        self.assertTrue(check_response(get_response(option)))

    def test_invalid_gc(self):
        (option, self.parser) = self.parser.parse_args(["--gc=23"])
        self.assertFalse(check_response(get_response(option)))

    def test_no_location(self):
        (option, self.parser) = self.parser.parse_args(["--temp=Celsius"])
        self.assertFalse(check_response(get_response(option)))

    def test_invalid_api(self):
        (option, self.parser) = self.parser.parse_args(["--api=thisIsInvalid"])
        self.assertFalse(check_response(get_response(option)))

    def test_city_not_found(self):
        (option, self.parser) = self.parser.parse_args(["--city=Melbonre"])
        self.assertFalse(check_response(get_response(option)))

class check_response_test(unittest.TestCase):
    def setUp(self):
        code_200_response = ({
            "message": "Mock valid response",
            "cod": 200
        })
        code_400_response = ({
            "message": "bad request",
            "cod": 400
        })
        code_401_response = ({
            "message": "Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.",
            "cod": 401
        })
        code_404_response = ({
            "message": "city not found",
            "cod": 404
        })
        code_429_response = ({
            "message": "API key blocked",
            "cod": 429
        })

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://400.response.url', json=code_400_response, status=400)
            self.code_400_Response = requests.get("http://400.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://401.response.url', json=code_401_response, status=401)
            self.code_401_Response = requests.get("http://401.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://404.response.url', json=code_404_response, status=404)
            self.code_404_Response = requests.get("http://404.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://429.response.url', json=code_429_response, status=429)
            self.code_429_Response = requests.get("http://429.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://200.response.url', json=code_200_response, status=200)
            self.code_200_Response = requests.get("http://200.response.url")

    def test_400(self):
        self.assertFalse(check_response(self.code_400_Response))

    def test_401(self):
        self.assertFalse(check_response(self.code_401_Response))

    def test_404(self):
        self.assertFalse(check_response(self.code_404_Response))

    def test_429(self):
        self.assertFalse(check_response(self.code_429_Response))

    def test_200(self):
        self.assertTrue(check_response(self.code_200_Response))

    def test_314(self):
        self.assertFalse(check_response(314))

class output_info_test(unittest.TestCase):

    def setUp(self):
        normal_response = ({
            "coord": {
                "lon": 144.96,
                "lat": -37.81
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10n"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 12.05,
                "pressure": 1009,
                "humidity": 87,
                "temp_min": 10.56,
                "temp_max": 13.89
            },
            "visibility": 10000,
            "wind": {
                "speed": 1.5,
                "deg": 140
            },
            "rain": {
                "3h": 0.126
            },
            "clouds": {
                "all": 26
            },
            "dt": 1571225078,
            "sys": {
                "type": 1,
                "id": 9548,
                "country": "AU",
                "sunrise": 1571168063,
                "sunset": 1571215023
            },
            "timezone": 39600,
            "id": 2158177,
            "name": "Melbourne",
            "cod": 200
        })
        cloudy_response = ({
            "coord": {
                "lon": 113.26,
                "lat": 23.13
            },
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "broken clouds",
                    "icon": "04n"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 25.7,
                "pressure": 1018,
                "humidity": 65,
                "temp_min": 25,
                "temp_max": 26.67
            },
            "visibility": 10000,
            "wind": {
                "speed": 3,
                "deg": 40
            },
            "rain": {},
            "clouds": {
                "all": 66
            },
            "dt": 1571231948,
            "sys": {
                "type": 1,
                "id": 9620,
                "country": "CN",
                "sunrise": 1571178226,
                "sunset": 1571220074
            },
            "timezone": 28800,
            "id": 1809858,
            "name": "Guangzhou",
            "cod": 200
        })
        no_degree_wind_response = ({
            "coord": {
                "lon": 144.96,
                "lat": -37.81
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10n"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 12.05,
                "pressure": 1009,
                "humidity": 87,
                "temp_min": 10.56,
                "temp_max": 13.89
            },
            "visibility": 10000,
            "wind": {
                "speed": 1.5
            },
            "rain": {
                "3h": 0.126
            },
            "clouds": {
                "all": 26
            },
            "dt": 1571225078,
            "sys": {
                "type": 1,
                "id": 9548,
                "country": "AU",
                "sunrise": 1571168063,
                "sunset": 1571215023
            },
            "timezone": 39600,
            "id": 2158177,
            "name": "Melbourne",
            "cod": 200
        })


        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://normal.response.url', json=normal_response, status=404)
            self.normalResponse = requests.get("http://normal.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://cloudy.response.url', json=cloudy_response, status=404)
            self.cloudyResponse = requests.get("http://cloudy.response.url")

        with responses.RequestsMock() as response:
            response.add(responses.GET, 'http://no.degree.wind.response.url', json=no_degree_wind_response, status=404)
            self.nodegreeWindResponse = requests.get("http://no.degree.wind.response.url")

        self.parser = weather_args()
        self.location = "somewhere"

    def test_time(self):
        (option,args) = self.parser.parse_args(["--time"])
        output = output_info(option,self.normalResponse,self.location)
        self.assertEqual(output,"\nOn 2019-10-16 22:24:38+11, the temperature in ["+self.location+"] ranges from 10.56 - 13.89 Celsius.\n")

    def test_temp_imperial(self):
        (option,args) = self.parser.parse_args(["--temp=Imperial"])
        output = output_info(option,self.normalResponse,self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Fahrenheit.\n")

    def test_temp_metric(self):
        (option, args) = self.parser.parse_args(["--temp=Metric"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output, "\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius.\n")

    def test_pressure(self):
        (option, args) = self.parser.parse_args(["--pressure"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output, "\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Atmospheric Pressure is at 1009hPa.\n")

    def test_not_cloudy(self):
        (option, args) = self.parser.parse_args(["--cloud"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output, "\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Cloud Density is 26%.\n")

    def test_cloudy(self):
        (option, args) = self.parser.parse_args(["--cloud"])
        output = output_info(option, self.cloudyResponse, self.location)
        self.assertEqual(output, "\nThe temperature in [" + self.location + "] ranges from 25 - 26.67 Celsius. Seeing broken clouds with about 66% coverage.\n")

    def test_humidity(self):
        (option, args) = self.parser.parse_args(["--humidity"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output, "\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Humidity is 87%.\n")

    def test_wind_with_degree_imperial(self):
        (option, args) = self.parser.parse_args(["--wind", "--temp=Imperial"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Fahrenheit. Wind is blowing at 1.5 miles/hr from 140 degrees.\n")

    def test_wind_with_degree_metric(self):
        (option, args) = self.parser.parse_args(["--wind"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Wind is blowing at 1.5 metres/s from 140 degrees.\n")

    def test_wind_without_degree_imperial(self):
        (option, args) = self.parser.parse_args(["--wind", "--temp=Imperial"])
        output = output_info(option, self.nodegreeWindResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Fahrenheit. Wind is blowing at 1.5 miles/hr.\n")

    def test_wind_without_degree_metric(self):
        (option, args) = self.parser.parse_args(["--wind"])
        output = output_info(option, self.nodegreeWindResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Wind is blowing at 1.5 metres/s.\n")

    def test_sunrise_and_sunset(self):
        (option, args) = self.parser.parse_args(["--sunrise","--sunset"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Sunrise is at 06:34:23+11, and Sunset is at 19:37:03+11.\n")

    def test_sunrise(self):
        (option, args) = self.parser.parse_args(["--sunrise"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Sunrise is at 06:34:23+11.\n")

    def test_sunset(self):
        (option, args) = self.parser.parse_args(["--sunset"])
        output = output_info(option, self.normalResponse, self.location)
        self.assertEqual(output,"\nThe temperature in [" + self.location + "] ranges from 10.56 - 13.89 Celsius. Sunset is at 19:37:03+11.\n")


if __name__ == "__main__":
    unittest.main()



