import time
import picamera2
from web_services import sendData, sendGSR
from grove.adc import ADC
import configparser


class GroveGSRSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value

Grove = GroveGSRSensor



def recordImageAndGSR():
    config = configparser.ConfigParser()
    config.read('config.ini')

    imageConfig = {
        "host": config.get('IMAGE', 'image_host'),
        "loresX": config.get('IMAGE', 'loresX'),
        "loresY": config.get('IMAGE', 'loresY'),
        "framerate": config.get('IMAGE', 'framerate'),
        "frequence": config.get('IMAGE', 'frequence'),
    }

    gsrConfig = {
        "host": config.get('GSR', 'gsr_host'),
        "frequence": config.get('GSR', 'frequence'),
    }

    loresX = int(imageConfig['loresX'])
    loresY = int(imageConfig['loresY'])


    #Camera configs
    camera = picamera2.Picamera2()
    camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (loresX, loresY)}, display="lores")
    camera.configure(camera_config)
    camera.framerate = imageConfig['framerate']
    camera.start()

    #GSR sensor
    sensor = GroveGSRSensor(0)

    #Recording
    while True:
        timestamp = int(time.time())  #Unic identifier

        try:
            sendGSR(sensor.GSR, gsrConfig['host'])   #Record and send GSR

            #Record and send image
            output = str(timestamp) + "-stream.jpg"
            camera.capture_file(output)
            sendData(imageConfig['host'], output, 'image')
        finally:
            time.sleep(float(imageConfig['frequence']))