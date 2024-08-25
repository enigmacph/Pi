import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(14, GPIO.IN)  # Set GPIO pin 14 as input (You can change this to any GPIO pin you are using)

try:
    print("KY-022 IR Receiver Test")
    print("Waiting for IR signal...")

    while True:
        if GPIO.input(14) == 0:  # Assuming the module outputs LOW when an IR signal is detected
            print("IR signal detected!")
            time.sleep(0.2)  # Add a small delay to avoid overwhelming the console with messages
        else:
            time.sleep(0.1)  # Add a small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
