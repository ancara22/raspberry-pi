
import math
import sys
import time
from grove.adc import ADC
from web_services import sendGSR


class GroveGSRSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value

Grove = GroveGSRSensor


def recordGSR():
    sensor = GroveGSRSensor(0)

    print('Detecting...')
    while True:
        print('GSR value: {0}'.format(sensor.GSR))
        time.sleep(.3)
        sendGSR(sensor.GSR, 'http://192.168.0.57:8080/gsr')


