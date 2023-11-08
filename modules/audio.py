import pyaudio
import wave
import time
from modules.web_services import sendData
import configparser


#Record audio from the microphone
def record_audio():
    #Get audio configurations from the config.ini
    config = configparser.ConfigParser()
    config.read('/home/rig/Documents/App/main/config.ini')

    #Set audio configuration
    audioConfig = {
        "host": config.get('audio', 'audio_host'),
        "frequence": config.get('audio', 'frequence'),
        "dev_index": config.get('audio', 'dev_index'),
        "samp_rate": config.get('audio', 'samp_rate'),
        "chunk": config.get('audio', 'chunk')
    }

    form_1 = pyaudio.paInt16 
    chans = 1
    samp_rate = int(audioConfig['samp_rate'])
    chunk = int(audioConfig['chunk'])
    record_secs = int(audioConfig['frequence'])
    dev_index = int(audioConfig['dev_index'])

    microphone = pyaudio.PyAudio()

    #Start recording cicle
    while True:
        #Record
        record = microphone.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, frames_per_buffer=chunk)

        timestamp = int(time.time())     #Get timestamp for unic names
        fileName = f"/home/rig/Documents/App/main/data/audio/audio_{timestamp}.wav"     #Directory path for file saving
        frames = []     #Audio frames container

        #Record frames and add to frames container
        for i in range(0, int((samp_rate/chunk)*record_secs)):
            data = record.read(chunk)
            frames.append(data)
        
        #Stop recording
        record.stop_stream()
        record.close()
        #microphone.terminate()

        # Save the final audio to a file
        wavefile = wave.open(fileName,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(microphone.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

        #Send the file to the server
        sendData(audioConfig['host'], fileName, "audio")


