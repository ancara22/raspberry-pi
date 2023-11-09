import time
import picamera2
from modules.web_services import sendData, sendGSR
from grove.adc import ADC
import configparser


#Grove GSR sensor initiating
class GroveGSRSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value

Grove = GroveGSRSensor

#Start paralel recording of images and gsr data
def recordImageAndGSR():
    #Get configurations from the config.ini
    config = configparser.ConfigParser()
    config.read('/home/rig/Documents/App/main/config.ini')

    #Set the image recording configurations 
    imageConfig = {
        "host": config.get("image", 'image_host'),
        "loresX": config.get("image", 'loresX'),
        "loresY": config.get("image", 'loresY'),
        "framerate": config.get("image", 'framerate'),
        "frequence": config.get("image", 'frequence'),
    }

    #Set the GSR recording configurations
    gsrConfig = {
        "host": config.get('GSR', 'gsr_host'),
        "frequence": config.get('GSR', 'frequence'),
    }

    #Image quality/resolution
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
            camera.capture_file("/home/rig/Documents/App/main/data/images/" + output)
            sendData(imageConfig['host'], output, 'image')
        finally:
            time.sleep(float(imageConfig['frequence']))
