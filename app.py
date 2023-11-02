from audio import record_audio
import threading
from thread1 import recordImageAndGSR


if __name__ == '__main__':
   thread1 = threading.Thread(target=recordImageAndGSR)
   thread2 = threading.Thread(target=record_audio)

   thread1.start()
   thread2.start()