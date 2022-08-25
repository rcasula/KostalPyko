import httpretty
import unittest
from kostalpiko.kostalpiko import Piko
import os

class Test551(unittest.TestCase):
    
    def setUp(self):
        httpretty.enable(verbose=True)  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET, "http://example.com/index.fhtml", body=open("./tests/fixtures/index55-1.html").read())
        self.piko = Piko(host='http://example.com')
        self.piko.update_data()
        # print("Test 5-5-1")

    def tearDown(self):
        httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
        httpretty.reset()  # reset HTTPretty state (clean up registered urls and request history)

    def test_get_raw_content(self):
        self.assertEqual(self.piko.data._raw_data,
                         ['112', '9290', '19.83', '384', '230', '0.20', '0', '278', '232', '0.21', '112', '0', '230',
                          '0.00', '0', 'Einspeisen MPP'])

    def test_get_current_power(self):
        self.assertEqual(self.piko.data.get_current_power(), 112)

    def test_get_total_energy(self):
        self.assertEqual(self.piko.data.get_total_energy(), 9290)

    def test_get_daily_energy(self):
        self.assertEqual(self.piko.data.get_daily_energy(), 19.83)

    def test_get_string1_voltage(self):
        self.assertEqual(self.piko.data.get_string1_voltage(), 384)

    def test_get_string2_voltage(self):
        self.assertEqual(self.piko.data.get_string2_voltage(), 278)

    def test_get_string3_voltage(self):
        self.assertEqual(self.piko.data.get_string3_voltage(), 0)

    def test_get_string1_current(self):
        self.assertEqual(self.piko.data.get_string1_current(), 0.2)

    def test_get_string2_current(self):
        self.assertEqual(self.piko.data.get_string2_current(), 0.21)

    def test_get_string3_current(self):
        self.assertEqual(self.piko.data.get_string3_current(), 0.0)

    def test_get_l1_voltage(self):
        self.assertEqual(self.piko.data.get_l1_voltage(), 230)

    def test_get_l2_voltage(self):
        self.assertEqual(self.piko.data.get_l2_voltage(), 232)

    def test_get_l3_voltage(self):
        self.assertEqual(self.piko.data.get_l3_voltage(), 230)

    def test_get_l1_power(self):
        self.assertEqual(self.piko.data.get_l1_power(), 0)

    def test_get_l2_power(self):
        self.assertEqual(self.piko.data.get_l2_power(), 112)

    def test_get_l3_power(self):
        self.assertEqual(self.piko.data.get_l3_power(), 0)
    
    def status(self):
        self.assertEqual(self.piko.data.get_status(), 'Einspeisen MPP')
