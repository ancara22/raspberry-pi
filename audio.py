import pyaudio
import wave
import os
import time
from web_services import sendData
import configparser

def record_audio():
    if not os.path.exists("audio"):
        os.mkdir("audio")

    config = configparser.ConfigParser()
    config.read('./config.ini')

    audioConfig = {
        "host": config.get('audio.config', 'audio_host'),
        "frequence": config.get('audio.config', 'frequence'),
        "dev_index": config.get('audio.config', 'dev_index'),
        "samp_rate": config.get('audio.config', 'samp_rate'),
        "chunk": config.get('audio.config', 'chunk')
    }

    form_1 = pyaudio.paInt16 
    chans = 1
    samp_rate = int(audioConfig['samp_rate'])
    chunk = int(audioConfig['chunk'])
    record_secs = int(audioConfig['frequence'])
    dev_index = int(audioConfig['dev_index'])

    

    microphone = pyaudio.PyAudio()

    while True:
        record = microphone.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, frames_per_buffer=chunk)

        timestamp = int(time.time())
        fileName = f"audio/audio_{timestamp}.wav"
        frames = []

        for i in range(0, int((samp_rate/chunk)*record_secs)):
            data = record.read(chunk)
            frames.append(data)
            
        record.stop_stream()
        record.close()
        #microphone.terminate()

        # Save to a file
        wavefile = wave.open(fileName,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(microphone.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

        sendData(audioConfig['host'], fileName, "audio")


