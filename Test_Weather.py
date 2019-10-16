import unittest
from unittest.mock import Mock
from optparse import OptionParser
from WeatherForecast import *
from unittest.mock import patch
import sys


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

    def test_city(self):
        (option, self.parser) = self.parser.parse_args(["--city=CITY"])
        self.assertTrue(check_num_of_location_input(option))

    def test_cid(self):
        (option, self.parser) = self.parser.parse_args(["--cid=code"])
        self.assertTrue(check_num_of_location_input(option))

    def test_gc(self):
        (option, self.parser) = self.parser.parse_args(['--gc=[23°01′0″ 113°07′0″]'])
        self.assertTrue(check_num_of_location_input(option))

    def test_z(self):
        (option, self.parser) = self.parser.parse_args(['-z=zipcode'])
        self.assertTrue(check_num_of_location_input(option))

    def test_no__location_input(self):
        (option, self.parser) = self.parser.parse_args(["--api=API"])
        self.assertFalse(check_num_of_location_input(option))

    def test_combination(self):
        (option, self.parser) = self.parser.parse_args(["--city=CITY", "--cid=CityID"])
        self.assertFalse(check_num_of_location_input(option))

class output_info_test(unittest.TestCase):
    def setUp(self):
        self.normalResponse = requests.get("http://www.mocky.io/v2/5da70169340000474763346f")
        self.cloudyResponse = requests.get("http://www.mocky.io/v2/5da718ef2f00005c0036824b")
        self.nodegreeWindResponse = requests.get("http://www.mocky.io/v2/5da71f6a2f000049003682a8")
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



