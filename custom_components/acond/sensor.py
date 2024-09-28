import requests
import xmltodict
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import TEMP_CELSIUS

# Define constants for the URL and authentication details
URL = "http://10.0.1.105/PAGE115.xml"
USERNAME = "acond"
PASSWORD = "acond"

def setup_platform(hass, config, add_entities, discovery_info=None):
    # Create a list of sensors and binary sensors
    sensors = [
        AcondSensor(name="Acond Outlet Water Temperature", url=URL, username=USERNAME, password=PASSWORD, field_name="__T9E13248E_REAL_.1f", unit=TEMP_CELSIUS),
        AcondSensor(name="Acond Return Water Temperature", url=URL, username=USERNAME, password=PASSWORD, field_name="__T50A32455_REAL_.1f", unit=TEMP_CELSIUS),
    ]
    
    binary_sensors = [
        AcondBinarySensor(name="Acond Mode Automatic", url=URL, username=USERNAME, password=PASSWORD, field_name="__T33F5FB04_BOOL_i"),
        AcondBinarySensor(name="Acond Mode Bivalent", url=URL, username=USERNAME, password=PASSWORD, field_name="__T3E1036AA_BOOL_i"),
    ]

    add_entities(sensors + binary_sensors)

class AcondSensor(SensorEntity):
    def __init__(self, name, url, username, password, field_name, unit):
        self._name = name
        self._url = url
        self._username = username
        self._password = password
        self._field_name = field_name
        self._unit = unit
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    def update(self):
        response = requests.get(self._url, auth=(self._username, self._password))
        if response.status_code == 200:
            data = xmltodict.parse(response.text)
            inputs = data['PAGE']['INPUT']
            value = next((item['@VALUE'] for item in inputs if item['@NAME'] == self._field_name), None)
            self._state = value
        else:
            self._state = None

class AcondBinarySensor(BinarySensorEntity):
    def __init__(self, name, url, username, password, field_name):
        self._name = name
        self._url = url
        self._username = username
        self._password = password
        self._field_name = field_name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state == '1'

    def update(self):
        response = requests.get(self._url, auth=(self._username, self._password))
        if response.status_code == 200:
            data = xmltodict.parse(response.text)
            inputs = data['PAGE']['INPUT']
            value = next((item['@VALUE'] for item in inputs if item['@NAME'] == self._field_name), None)
            self._state = value
        else:
            self._state = None
