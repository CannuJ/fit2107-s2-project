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
        (option, self.parser) = self.parser.parse_args(['--gc=[23°01′0″ 113°07′0″]'])
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



if __name__ == "__main__":
    unittest.main()



