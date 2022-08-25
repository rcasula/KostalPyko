import httpretty
import unittest
from kostalpiko.kostalpiko import Piko
import os

class Test551(unittest.TestCase):
    
    def setUp(self):
        httpretty.enable(verbose=True)  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET, "http://example.com/index.fhtml", body=open("./tests/fixtures/index2-1.html").read())
        self.piko = Piko(host='http://example.com')
        self.piko.update_data()
        # print("Test 2-1")

    def tearDown(self):
        httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
        httpretty.reset()  # reset HTTPretty state (clean up registered urls and request history)

    def test_get_raw_content(self):
        self.assertEqual(self.piko.data._raw_data,
                         ['2336', '33523', '11.71', '338', '236', '3.88', '2336', '336', '3.97', 'supply MPP'])

    def test_get_current_power(self):
        self.assertEqual(self.piko.data.get_current_power(), 2336)

    def test_get_total_energy(self):
        self.assertEqual(self.piko.data.get_total_energy(), 33523)

    def test_get_daily_energy(self):
        self.assertEqual(self.piko.data.get_daily_energy(), 11.71)

    def test_get_string1_voltage(self):
        self.assertEqual(self.piko.data.get_string1_voltage(), 338)

    def test_get_string2_voltage(self):
        self.assertEqual(self.piko.data.get_string2_voltage(), 336)

    def test_get_string1_current(self):
        self.assertEqual(self.piko.data.get_string1_current(), 3.88)

    def test_get_string2_current(self):
        self.assertEqual(self.piko.data.get_string2_current(), 3.97)

    def test_get_l1_voltage(self):
        self.assertEqual(self.piko.data.get_l1_voltage(), 236)

    def test_get_l1_power(self):
        self.assertEqual(self.piko.data.get_l1_power(), 2336)

    def status(self):
        self.assertEqual(self.piko.data.get_status(), 'supply MPP')
