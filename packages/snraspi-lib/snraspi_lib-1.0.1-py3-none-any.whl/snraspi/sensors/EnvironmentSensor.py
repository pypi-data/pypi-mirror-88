#!/usr/bin/python3
#MIT License
#
#Copyright (c) 2020 signag
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
"""Module EnvironmentSensor

This module includes classes for an abstraction of environment sensors.
Supportet sensors are:
- DHT11
- DHT22
- BME280
"""
import board
import adafruit_dht
import inspect

#Setup logging
import logging
import logging_plus
logger = logging_plus.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class EnvironmentSensorError(Exception):
    """
    Base exception class for this module
    """
    pass

class EnvironmentSensorInstantiationError(EnvironmentSensorError):
    """
    A function has instatiated the general EnvironmentSensor rather than a specific one
    """
    def __init__(self):
        self.message = "You need to instantiate a specific EnvironmentSensor rather than the general."
        

class EnvironmentSensor:
    """
    Class representing an environment sensor
    """
    def __init__(self):
        """
        Constructor for EnvironmentSensor
        """
        self.__hasTemperature = False
        self.__hasHumidity = False
        self.__hasAltitude = False
        self.__hasPressure = False
        self.__sensor = None

    def __del__(self):
        self.terminate()

    def terminate(self):
        pass

    @property
    def temperature(self):
        """
        Return measured temperature in ° Celsius
        """

        if self.__sensor == None:
            raise EnvironmentSensorInstantiationError

        logger.debug("__hasTemperature: %s", self.__hasTemperature)        
        
        if self.__hasTemperature:
            return self.__sensor.temperature
        else:
            return None
    
    @property
    def humidity(self):
        """
        Return measured humidity
        """

        if self.__sensor == None:
            raise EnvironmentSensorInstantiationError

        logger.debug("__hasTemperature: %s", self.__hasHumidity)        
        
        if self.__hasHumidity:
            return self.__sensor.humidity
        else:
            return None
    
    @property
    def pressure(self):
        """
        Return measured pressure
        """

        if self.__sensor == None:
            raise EnvironmentSensorInstantiationError

        logger.debug("__hasPressure: %s", self.__hasPressure)        
        
        if self.__hasPressure:
            return self.__sensor.pressure
        else:
            return None
    
    @property
    def altitude(self):
        """
        Return measured altitude
        """

        if self.__sensor == None:
            raise EnvironmentSensorInstantiationError

        logger.debug("    __hasAltitude: %s", self.__hasAltitude)        
        
        if self.__hasAltitude:
            return self.__sensor.altitude
        else:
            return None

class DHT22(EnvironmentSensor):
    """
    Class representing the DHT22 sensor for measuring temperature and humidity
    """
    def __init__(self, oneWirePin):
        """
        Constructor for class DHT22:

        Attributes:
        - oneWirePin : GPIO pin (BOARD notation) connected to DHT22 data
        """
        logger.debug("oneWirePin.id: %s", oneWirePin.id)
        
        logger.debug("importing adafruit_dht")
        import adafruit_dht

        super().__init__()

        self._EnvironmentSensor__sensorType = "DHT22"

        self._EnvironmentSensor__oneWirePin = oneWirePin
        self._EnvironmentSensor__sensor = adafruit_dht.DHT22(self._EnvironmentSensor__oneWirePin, use_pulseio=False)

        self._EnvironmentSensor__hasTemperature = True
        self._EnvironmentSensor__hasHumidity = True

    def __del__(self):
        self.terminate()
        super().__del__()

    def terminate(self):
        self._EnvironmentSensor__sensor.exit()

class DHT11(EnvironmentSensor):
    """
    Class representing the DHT11 sensor for measuring temperature and humidity
    """
    def __init__(self, oneWirePin):
        """
        Constructor for class DHT11:

        Attributes:
        - oneWirePin : GPIO pin (BOARD notation) connected to DHT22 data
        """
        logger.debug("    oneWirePin.id: %s", oneWirePin.id)

        logger.debug("    importing adafruit_dht")
        import adafruit_dht

        super().__init__()

        self._EnvironmentSensor__sensorType = "DHT11"

        self._EnvironmentSensor__oneWirePin = oneWirePin
        self._EnvironmentSensor__sensor = adafruit_dht.DHT11(self._EnvironmentSensor__oneWirePin, use_pulseio=False)

        self._EnvironmentSensor__hasTemperature = True
        self._EnvironmentSensor__hasHumidity = True

    def __del__(self):
        self.terminate()
        super().__del__()

    def terminate(self):
        self._EnvironmentSensor__sensor.exit()

class BME280_I2C(EnvironmentSensor):
    """
    Class representing the BME280 sensor using I2C bus
    for measuring temperature, humidity, pressure and altitude
    """
    def __init__(self):
        """
        Constructor for class EnvironmentSensorBME289_I2C
        """
        logger.debug("    importing adafruit digitalio, busio, adafruit_bme280")
        import digitalio
        import busio
        import adafruit_bme280

        super().__init__()

        self._EnvironmentSensor__sensorType = "BME280"

        # Get the I2C bus
        self._EnvironmentSensor__i2c = busio.I2C(board.SCL, board.SDA)
        self._EnvironmentSensor__sensor = adafruit_bme280.Adafruit_BME280_I2C(self._EnvironmentSensor__i2c)

        self._EnvironmentSensor__hasTemperature = True
        self._EnvironmentSensor__hasHumidity = True
        self._EnvironmentSensor__hasPressure = True
        self._EnvironmentSensor__hasAltitude = True

class BME280_SPI(EnvironmentSensor):
    """
    Class representing the BME280 sensor using SPI bus
    for measuring temperature, humidity, pressure and altitude
    """
    def __init__(self, chipSelectPin):
        """
        Constructor for class BME280_SPI
        """
        logger.debug("chipSelectPin.id: %s", chipSelectPin.id)
        logger.debug("importing adafruit digitalio, busio, adafruit_bme280")
        import digitalio
        import busio
        import adafruit_bme280

        super().__init__()

        self._EnvironmentSensor__sensorType = "BME280"
        self._EnvironmentSensor__chipSelectPin = chipSelectPin

        # Get the SPI bus
        self._EnvironmentSensor__spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self._EnvironmentSensor__bme_cs = digitalio.DigitalInOut(self._EnvironmentSensor__chipSelectPin)
        self._EnvironmentSensor__sensor = adafruit_bme280.Adafruit_BME280_SPI(self._EnvironmentSensor__spi, self._EnvironmentSensor__bme_cs)

        self._EnvironmentSensor__hasTemperature = True
        self._EnvironmentSensor__hasHumidity = True
        self._EnvironmentSensor__hasPressure = True
        self._EnvironmentSensor__hasAltitude = True

# List of available GPIO pins in BOARD (pin) numbering
# Pin numbering is converted to adafruit board objects
PIN03 = board.D2
PIN05 = board.D3
PIN07 = board.D4
PIN08 = board.D14
PIN10 = board.D15
PIN11 = board.D17
PIN12 = board.D18
PIN13 = board.D27
PIN15 = board.D22
PIN16 = board.D23
PIN18 = board.D24
PIN19 = board.D10
PIN21 = board.D9
PIN22 = board.D25
PIN23 = board.D11
PIN24 = board.D8
PIN26 = board.D7
PIN27 = board.D0
PIN28 = board.D1
PIN29 = board.D5
PIN31 = board.D6
PIN32 = board.D12
PIN33 = board.D13
PIN35 = board.D19
PIN36 = board.D16
PIN37 = board.D26
PIN38 = board.D20
PIN40 = board.D21
