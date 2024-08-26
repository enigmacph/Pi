import RPi.GPIO as GPIO
import time


# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(14, GPIO.IN)  # Set GPIO pin 14 as input (You can change this to any GPIO pin you are using)

while True:
    if GPIO.input(14) == 0:  # Assuming the module outputs LOW when an IR signal is detected
        print("IR signal detected!")
        time.sleep(0.2)  # Add a small delay to avoid overwhelming the console with messages
    else:
        time.sleep(0.1)  # Add a small delay to prevent excessive CPU usage


pi = pigpio.pi()
ir = ir_decoder.IRDecoder(pi, GPIO_PIN)