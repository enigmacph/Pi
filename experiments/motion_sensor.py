import RPi.GPIO as GPIO
import time

# Audio
import soco
import schedule
import time

den = soco.SoCo('192.168.50.198')
den.volume=80

def play_sound():
    try:
        den.play_uri("http://192.168.50.252/obi-wan-hello-there.mp3")
    except:
        print("error wrt. sonos")

# Set up GPIO
PIR_PIN = 25  # GPIO pin connected to the PIR OUT
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)  # Give time for the sensor to stabilize
    print("Ready")

    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
            play_sound()
        time.sleep(5)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
