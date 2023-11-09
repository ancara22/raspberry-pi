import os
import threading
from modules.audio_recorder import startRecordingListener
from modules.image_gsr_recorder import recordImageAndGSR


# Remove the files that stuk in the system because of the app stop
def cleanJunkFiles(directory_path, file_type):
   try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            #Check if the file is type of file_type
            if os.path.isfile(file_path) and filename.lower().endswith(file_type):
                os.remove(file_path)

   except Exception as e:
        print(f"Error: {e}")


#Rund the app
if __name__ == '__main__':
   cleanJunkFiles("/home/rig/Documents/App/main/data/audio", ".wav")     # Remove the audio files
   cleanJunkFiles("/home/rig/Documents/App/main/data/images", ".jpg")    # Remove the jpg files

   thread1 = threading.Thread(target=recordImageAndGSR)        # Image and GSR recording
   thread2 = threading.Thread(target=startRecordingListener)   # Live Speech detection and audio recording

   thread1.start()
   thread2.start()





