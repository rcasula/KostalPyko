#!/usr/bin/env python


"""Library to work with a Piko inverter from Kostal."""
import logging
import requests
from lxml import html
from .utils import safe_list_get
from .const import *

LOG = logging.getLogger(__name__)

class Piko:
    def __init__(self, host=None, username="pvserver", password="pvwr"):
        self.host = host
        self.username = username
        self.password = password
        self.data = None
        self.ba_data = None

    def update(self):
        """updates all data"""
        self.update_data()
        self.update_ba_data()

    def update_data(self):
        """updates data"""
        try:
            data = self._get_raw_content()
            if data is not None:
                self.data = PikoData(data)
        except Exception as err:
            LOG.debug(err)
            pass

    def update_ba_data(self):
        """updates ba data"""
        try:
            data = self._get_content_of_own_consumption()
            if data is not None:
                self.ba_data = PikoBAData(data)
        except Exception as err:
            LOG.debug(err)
            pass

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
            LOG.error(errc)
            return None
        except requests.exceptions.Timeout as errt:
            LOG.error(errt)
            return

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

    def get_logdaten_dat(self):
        pass


class PikoData(object):
    """
    PIKO Data
    """

    def __init__(self, raw_data):
        self._raw_data = raw_data
        n_values = len(raw_data)
        if n_values == 8:
            self.indices = SINGLE_STRING_INDICES
        elif n_values == 10:
            self.indices = DOUBLE_STRING_SINGLE_PHASE_INDICES
        elif n_values == 12:
            self.indices = DOUBLE_STRING_TWO_PHASES_INDICES
        elif n_values == 14:
            self.indices = DOUBLE_STRING_THREE_PHASES_INDICES
        elif n_values == 16:
            self.indices = TRIPLE_STRING_INDICES

    def safe_get_value(self, name):
        if self._raw_data is not None and name in self.indices and self.indices[name] is not None:
            return safe_list_get(self._raw_data, self.indices[name])

    def get_current_power(self):
        """returns the current power in W"""
        value = self.safe_get_value('current_power')
        if value is not None:
            return int(value)
        else:
            return None

    def get_total_energy(self):
        """returns the total energy in kWh"""
        value = self.safe_get_value('total_energy')
        if value is not None:
            return int(value)
        else:
            return None

    def get_daily_energy(self):
        """returns the daily energy in kWh"""
        value = self.safe_get_value('daily_energy')
        if value is not None:
            return float(value)
        else:
            return None

    def get_string1_voltage(self):
        """returns the voltage from string 1 in V"""
        value = self.safe_get_value('string1_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_string1_current(self):
        """returns the current from string 1 in A"""
        value = self.safe_get_value('string1_current')
        if value is not None:
            return float(value)
        else:
            return None

    def get_string2_voltage(self):
        """returns the voltage from string 2 in V"""
        value = self.safe_get_value('string2_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_string2_current(self):
        """returns the current from string 2 in A"""
        value = self.safe_get_value('string2_current')
        if value is not None:
            return float(value)
        else:
            return None

    def get_string3_voltage(self):
        """returns the voltage from string 3 in V"""
        value = self.safe_get_value('string3_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_string3_current(self):
        """returns the current from string 3 in A"""
        value = self.safe_get_value('string3_current')
        if value is not None:
            return float(value)
        else:
            return None

    def get_l1_voltage(self):
        """returns the voltage from line 1 in V"""
        value = self.safe_get_value('l1_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_l1_power(self):
        """returns the power from line 1 in W"""
        value = self.safe_get_value('l1_power')
        if value is not None:
            return int(value)
        else:
            return None

    def get_l2_voltage(self):
        """returns the voltage from line 2 in V"""
        value = self.safe_get_value('l2_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_l2_power(self):
        """returns the power from line 1 in W"""
        value = self.safe_get_value('l2_power')
        if value is not None:
            return int(value)
        else:
            return None

    def get_l3_voltage(self):
        """returns the voltage from line 3 in V"""
        value = self.safe_get_value('l3_voltage')
        if value is not None:
            return int(value)
        else:
            return None

    def get_l3_power(self):
        value = self.safe_get_value('l3_power')
        if value is not None:
            return int(value)
        else:
            return None

    def get_piko_status(self):
        """returns the power from line 3 in W"""
        value = self.safe_get_value('status')
        if value is not None:
            return value
        else:
            return None


class PikoBAData(object):
    """
    PIKO BA Data
    """

    def __init__(self, raw_data):
        self._raw_data = raw_data

    def get_solar_generator_power(self):
        """returns the current power of the solar generator in W"""
        if self._raw_data:
            return safe_list_get(self._raw_data, 5)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_1(self):
        """returns the current consumption of phase 1 in W"""
        if self._raw_data:
            return safe_list_get(self._raw_data, 8)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_2(self):
        """returns the current consumption of phase 2 in W"""
        if self._raw_data:
            return safe_list_get(self._raw_data, 9)
        else:
            return "No BA sensor installed"

    def get_consumption_phase_3(self):
        """returns the current consumption of phase 3 in W"""
        if self._raw_data:
            return safe_list_get(self._raw_data, 10)
        else:
            return "No BA sensor installed"
