import RPi.GPIO as GPIO
import time

# Audio
import soco
import schedule
import time

def play_sound():
    try:
        den = soco.SoCo('192.168.50.198')
        den.volume=80
        den.play_uri("http://192.168.50.252/obi-wan-hello-there.mp3")
    except:
        print("error wrt. sonos")

# Set up GPIO
PIR_PIN = 25  # GPIO pin connected to the PIR OUT
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

time.sleep(2)  # Give time for the sensor to stabilize

while True:
    if GPIO.input(PIR_PIN):
        play_sound()
        time.sleep(5)
    time.sleep(1)