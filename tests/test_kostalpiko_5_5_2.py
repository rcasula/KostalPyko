import httpretty
import unittest
from kostalpiko.kostalpiko import Piko
import os

class Test551(unittest.TestCase):
    
    def setUp(self):
        httpretty.enable(verbose=True)  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET, "http://example.com/index.fhtml", body=open("./tests/fixtures/index55-2.html").read())
        self.piko = Piko(host='http://example.com')
        self.piko.update_data()
        # print("Test 5-5-2")

    def tearDown(self):
        httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
        httpretty.reset()  # reset HTTPretty state (clean up registered urls and request history)

    def test_get_raw_content(self):
        self.assertEqual(self.piko.data._raw_data,
                         ['3126', '41801', '13.46', 
                         '275', '247', 
                         '6.27', '1032', 
                         '247', '241', 
                         '6.47', '1027', 
                         '0', '246',
                         '0.00', '1069', 
                         'toevoer MPP'])

    def test_get_current_power(self):
        self.assertEqual(self.piko.data.get_current_power(), 3126)

    def test_get_total_energy(self):
        self.assertEqual(self.piko.data.get_total_energy(), 41801)

    def test_get_daily_energy(self):
        self.assertEqual(self.piko.data.get_daily_energy(), 13.46)

    def test_get_string1_voltage(self):
        self.assertEqual(self.piko.data.get_string1_voltage(), 275)

    def test_get_string2_voltage(self):
        self.assertEqual(self.piko.data.get_string2_voltage(), 247)

    def test_get_string3_voltage(self):
        self.assertEqual(self.piko.data.get_string3_voltage(), 0)

    def test_get_string1_current(self):
        self.assertEqual(self.piko.data.get_string1_current(), 06.27)

    def test_get_string2_current(self):
        self.assertEqual(self.piko.data.get_string2_current(), 6.47)

    def test_get_string3_current(self):
        self.assertEqual(self.piko.data.get_string3_current(), 0.0)

    def test_get_l1_voltage(self):
        self.assertEqual(self.piko.data.get_l1_voltage(), 247)

    def test_get_l2_voltage(self):
        self.assertEqual(self.piko.data.get_l2_voltage(), 241)

    def test_get_l3_voltage(self):
        self.assertEqual(self.piko.data.get_l3_voltage(), 246)

    def test_get_l1_power(self):
        self.assertEqual(self.piko.data.get_l1_power(), 1032)

    def test_get_l2_power(self):
        self.assertEqual(self.piko.data.get_l2_power(), 1027)

    def test_get_l3_power(self):
        self.assertEqual(self.piko.data.get_l3_power(), 1069)
    
    def status(self):
        self.assertEqual(self.piko.data.get_status(), 'toevoer MPP')
