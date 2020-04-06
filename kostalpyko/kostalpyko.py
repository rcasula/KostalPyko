#!/usr/bin/env python


"""Library to work with a Piko inverter from Kostal."""
import logging

from lxml import html

# HTTP libraries depends upon Python 2 or 3
import requests

LOG = logging.getLogger(__name__)

class Piko:
    def __init__(self, host=None, username='pvserver', password='pvwr'):
        self.host = host
        self.username = username
        self.password = password

    def get_solar_generator_power(self):
        """returns the current power of the solar generator in W"""
        if self._get_content_of_own_consumption():
            return self._get_content_of_own_consumption()[5]
        else:
            return "No BA sensor installed"

    def get_consumption_phase_1(self):
        """returns the current consumption of phase 1 in W"""
        if self._get_content_of_own_consumption():
            return self._get_content_of_own_consumption()[8]
        else:
            return "No BA sensor installed"

    def get_consumption_phase_2(self):
        """returns the current consumption of phase 2 in W"""
        if self._get_content_of_own_consumption():
            return self._get_content_of_own_consumption()[9]
        else:
            return "No BA sensor installed"

    def get_consumption_phase_3(self):
        """returns the current consumption of phase 3 in W"""
        if self._get_content_of_own_consumption():
            return self._get_content_of_own_consumption()[10]
        else:
            return "No BA sensor installed"

    def _get_content_of_own_consumption(self):
        """returns all values as a list"""
        url = self.host + '/BA.fhtml'
        login = self.username
        pwd = self.password
        try:
            r = requests.get(url, auth=(login, pwd), timeout=15)
            if r.status_code == 200:
                response = html.fromstring(r.content)
                data = []
                for v in response.xpath("//b"):
                    raw = v.text.strip()
                    raw = raw[:-1]  # remove unit
                    try:
                        value = float(raw)
                    except:
                        value = 0
                    data.append(value)
                LOG.debug("content_of_own_consumption:", data)
                return data
            else:
                raise ConnectionError
        except requests.exceptions.ConnectionError as errc:
            return None
        except requests.exceptions.Timeout as errt:
            return None

    def get_logdaten_dat(self):
        pass

    def get_current_power(self):
        """returns the current power in W"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[0])

    def get_total_energy(self):
        """returns the total energy in kWh"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[1])

    def get_daily_energy(self):
        """returns the daily energy in kWh"""
        if self._get_raw_content() is not None:
            return float(self._get_raw_content()[2])

    def get_string1_voltage(self):
        """returns the voltage from string 1 in V"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[3])

    def get_string1_current(self):
        """returns the current from string 1 in A"""
        if self._get_raw_content() is not None:
            return float(self._get_raw_content()[5])

    def get_string2_voltage(self):
        """returns the voltage from string 2 in V"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[7])

    def get_string2_current(self):
        """returns the current from string 2 in A"""
        if self._get_raw_content() is not None:
            return float(self._get_raw_content()[9])

    def get_string3_voltage(self):
        """returns the voltage from string 3 in V"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # String 3 not installed
            return None
        else:
            return int(raw_content[11])

    def get_string3_current(self):
        """returns the current from string 3 in A"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # String 3 not installed
            return None
        else:
            return float(raw_content[13])

    def get_l1_voltage(self):
        """returns the voltage from line 1 in V"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[4])

    def get_l1_power(self):
        """returns the power from line 1 in W"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[6])

    def get_l2_voltage(self):
        """returns the voltage from line 2 in V"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[8])

    def get_l2_power(self):
        """returns the power from line 1 in W"""
        if self._get_raw_content() is not None:
            return int(self._get_raw_content()[10])

    def get_l3_voltage(self):
        """returns the voltage from line 3 in V"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            return int(raw_content[11])
        else:
            # 3 Strings
            return int(raw_content[12])

    def get_l3_power(self):
        """returns the power from line 3 in W"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            return int(raw_content[12])
        else:
            # 3 Strings
            return int(raw_content[14])

    def get_piko_status(self):
        """returns the power from line 3 in W"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            return raw_content[13]
        else:
            # 3 Strings
            return int(raw_content[15])

    def _get_raw_content(self):
        """returns all values as a list"""
        url = self.host + '/index.fhtml'
        login = self.username
        pwd = self.password
        try:
            r = requests.get(url, auth=(login, pwd), timeout=15)
            LOG.debug("status_code:", r.status_code)
            # print("status_code:", r.status_code)
            if r.status_code == 200:
                response = html.fromstring(r.content)
                data = []
                for v in response.xpath("//td[@bgcolor='#FFFFFF']"):
                    raw = v.text.strip()
                    if 'x x x' in raw:
                        raw = 0
                    data.append(raw)
                status = response.xpath("/html/body/form/font/table[2]/tr[8]/td[3]")[0].text.strip()
                data.append(status)
                LOG.debug("raw_content:", data)
                # print("raw_content:", data)
                return data
            else:
                raise ConnectionError
        except requests.exceptions.ConnectionError as errc:
            LOG.debug("ConnectionError", errc)
            return None
        except requests.exceptions.Timeout as errt:
            LOG.debug("Timeout", errt)
            return None
            