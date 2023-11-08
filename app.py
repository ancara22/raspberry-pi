import threading
from modules.audio import record_audio
from modules.thread1 import recordImageAndGSR


#Rund the app
if __name__ == '__main__':
   thread1 = threading.Thread(target=recordImageAndGSR)
   thread2 = threading.Thread(target=record_audio)

   #Start the treads
   thread1.start()   
   thread2.start()