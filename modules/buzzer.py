from grove.gpio import GPIO
import time 

buzzer_pin = 12 #Port

# Initialize the GPIO
buzzer = GPIO(buzzer_pin, GPIO.OUT)

# Emit a long sound
def emit_long_sound():
    buzzer.write(1)
    time.sleep(2)
    buzzer.write(0)

# Emit a medium sound
def emit_medium_sound():
    buzzer.write(1)
    time.sleep(1)
    buzzer.write(0)

# Emit a short sound
def emit_short_sound():
    buzzer.write(1)
    time.sleep(0.5)
    buzzer.write(0)


def emit_start_sound():
    emit_long_sound()
    emit_medium_sound()
    emit_short_sound()