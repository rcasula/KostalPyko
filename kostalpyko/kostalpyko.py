#!/usr/bin/env python


"""Library to work with a Piko inverter from Kostal."""
import logging

# HTTP libraries depends upon Python 2 or 3
import requests
from lxml import html

LOG = logging.getLogger(__name__)


class Piko:
    def __init__(self, host=None, username="pvserver", password="pvwr"):
        self.host = host
        self.username = username
        self.password = password

    def get_solar_generator_power(self):
        """returns the current power of the solar generator in W"""
        if self._get_content_of_own_consumption():
            return self.safe_list_get(self._get_content_of_own_consumption(), 5)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_1(self):
        """returns the current consumption of phase 1 in W"""
        if self._get_content_of_own_consumption():
            return self.safe_list_get(self._get_content_of_own_consumption(), 8)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_2(self):
        """returns the current consumption of phase 2 in W"""
        if self._get_content_of_own_consumption():
            return self.safe_list_get(self._get_content_of_own_consumption(), 9)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_3(self):
        """returns the current consumption of phase 3 in W"""
        if self._get_content_of_own_consumption():
            return self.safe_list_get(self._get_content_of_own_consumption(), 10)
        else:
            return "No BA sensor installed"

    def _get_content_of_own_consumption(self):
        """returns all values as a list"""
        url = self.host + "/BA.fhtml"
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
                LOG.debug(data)
                return data
            else:
                raise ConnectionError
        except requests.exceptions.ConnectionError as errc:
            LOG.debug(errc)
            return None
        except requests.exceptions.Timeout as errt:
            LOG.debug(errt)
            return None

    def get_logdaten_dat(self):
        pass

    def get_current_power(self):
        """returns the current power in W"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 0)
            if value is not None:
                return int(value)
            else:
                return None

    def get_total_energy(self):
        """returns the total energy in kWh"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 1)
            if value is not None:
                return int(value)
            else:
                return None

    def get_daily_energy(self):
        """returns the daily energy in kWh"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 2)
            if value is not None:
                return float(value)
            else:
                return None

    def get_string1_voltage(self):
        """returns the voltage from string 1 in V"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 3)
            if value is not None:
                return int(value)
            else:
                return None

    def get_string1_current(self):
        """returns the current from string 1 in A"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 5)
            if value is not None:
                return float(value)
            else:
                return None

    def get_string2_voltage(self):
        """returns the voltage from string 2 in V"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 7)
            if value is not None:
                return int(value)
            else:
                return None

    def get_string2_current(self):
        """returns the current from string 2 in A"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 9)
            if value is not None:
                return float(value)
            else:
                return None

    def get_string3_voltage(self):
        """returns the voltage from string 3 in V"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # String 3 not installed
            return None
        else:
            value = self.safe_list_get(raw_content, 11)
            if value is not None:
                return int(value)
            else:
                return None

    def get_string3_current(self):
        """returns the current from string 3 in A"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # String 3 not installed
            return None
        else:
            value = self.safe_list_get(raw_content, 13)
            if value is not None:
                return float(value)
            else:
                return None

    def get_l1_voltage(self):
        """returns the voltage from line 1 in V"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 4)
            if value is not None:
                return int(value)
            else:
                return None

    def get_l1_power(self):
        """returns the power from line 1 in W"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 6)
            if value is not None:
                return int(value)
            else:
                return None

    def get_l2_voltage(self):
        """returns the voltage from line 2 in V"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 8)
            if value is not None:
                return int(value)
            else:
                return None

    def get_l2_power(self):
        """returns the power from line 1 in W"""
        if self._get_raw_content() is not None:
            value = self.safe_list_get(self._get_raw_content(), 10)
            if value is not None:
                return int(value)
            else:
                return None

    def get_l3_voltage(self):
        """returns the voltage from line 3 in V"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            value = self.safe_list_get(raw_content, 11)
            if value is not None:
                return int(value)
            else:
                return None
        else:
            # 3 Strings
            value = self.safe_list_get(raw_content, 12)
            if value is not None:
                return int(value)
            else:
                return None

    def get_l3_power(self):
        """returns the power from line 3 in W"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            value = self.safe_list_get(raw_content, 12)
            if value is not None:
                return int(value)
            else:
                return None
        else:
            # 3 Strings
            value = self.safe_list_get(raw_content, 14)
            if value is not None:
                return int(value)
            else:
                return None

    def get_piko_status(self):
        """returns the power from line 3 in W"""
        raw_content = self._get_raw_content()
        if len(raw_content) < 15:
            # 2 Strings
            return self.safe_list_get(raw_content, 13)
        else:
            # 3 Strings
            value = self.safe_list_get(raw_content, 15)
            if value is not None:
                return int(value)
            else:
                return None

    def _get_raw_content(self):
        """returns all values as a list"""
        url = self.host + "/index.fhtml"
        login = self.username
        pwd = self.password
        try:
            r = requests.get(url, auth=(login, pwd), timeout=15)
            if r.status_code == 200:
                response = html.fromstring(r.content)
                data = []
                for v in response.xpath("//td[@bgcolor='#FFFFFF']"):
                    raw = v.text.strip()
                    if "x x x" in raw:
                        raw = 0
                    data.append(raw)
                status = response.xpath("/html/body/form/font/table[2]/tr[8]/td[3]")[
                    0
                ].text.strip()
                data.append(status)
                LOG.debug(data)
                return data
            else:
                raise ConnectionError
        except requests.exceptions.ConnectionError as errc:
            LOG.debug(errc)
            return None
        except requests.exceptions.Timeout as errt:
            LOG.debug(errt)
            return None

    def _get_info(self):
        """returns the info about the inverter"""
        url = self.host + "/Solar2.fhtml"
        login = self.username
        pwd = self.password
        try:
            r = requests.get(url, auth=(login, pwd), timeout=15)
            if r.status_code == 200:
                response = html.fromstring(r.content)
                data = []
                serial = response.xpath("/html/body/form/font/table/tr[2]/td[3]")[
                    0
                ].text.strip()
                data.append(serial)
                model = response.xpath("/html/body/form/table/tr[2]/td[2]/font[1]")[
                    0
                ].text.strip()
                data.append(model)
                LOG.debug(data)
                return data
            else:
                raise ConnectionError
        except requests.exceptions.ConnectionError as errc:
            LOG.debug(errc)
            return None
        except requests.exceptions.Timeout as errt:
            LOG.debug(errt)
            return None

    def safe_list_get(self, l, idx, default = None):
        try:
            return l[idx]
        except IndexError:
            return default