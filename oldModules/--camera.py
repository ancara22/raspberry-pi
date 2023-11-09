import time
import picamera2
from main.modules.web_services import sendData
from picamera2.encoders import H264Encoder
import configparser


#Record images
def captureImage():
    config = configparser.ConfigParser()
    config.read('config.ini')

    imageConfig = {
        "host": config.get('IMAGE', 'image_host'),
        "mainSize": config.get('IMAGE', 'size'),
        "lores": config.get('IMAGE', 'lores'),
        "framerate": config.get('IMAGE', 'framerate'),
        "frequence": config.get('IMAGE', 'frequence'),
    }

    camera = picamera2.Picamera2()
    camera_config = camera.create_still_configuration(main={"size": imageConfig["mainSize"]}, lores={"size": imageConfig["lores"]}, display="lores")
    camera.configure(camera_config)
    camera.framerate = imageConfig["framerate"]
    camera.start()

    while True:
        timestamp = int(time.time())
        try:
            output = str(timestamp) + "-stream.jpg"
            camera.capture_file(output)
            sendData(imageConfig["host"], output, 'image')
        finally:
            time.sleep(imageConfig["frequence"]) 

#To be removed
#################################################
#Record videos
def captureVideo():
    picam2 = picamera2.Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)

    while True:
        timestamp = int(time.time()) 
        output = f"{timestamp}-video.h264" 

        try:
            picam2.start_recording(encoder, output)
            time.sleep(15)
            picam2.stop_recording()

            sendData('http://192.168.0.57:8080/video', output, 'video')
        finally:
            time.sleep(0.1)

#################################################

