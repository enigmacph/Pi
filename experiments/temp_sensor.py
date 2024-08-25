import Adafruit_DHT
import time

# Set sensor type : Options are DHT11, DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO pin where the data pin of DHT11 is connected
pin = 4  # Replace with the GPIO pin number you used (e.g., GPIO4 corresponds to pin 7)

# Audio
import soco
import schedule
import time

def play_sound():
    try:
        den = soco.SoCo('192.168.50.198')
        den.volume=80
        den.play_uri("http://192.168.50.252/you-know-whats-cooking.mp3")
    except:
        print("error wrt. sonos")

def read_dht11():
    global last_played_time
    # Try to get a sensor reading. The read_retry method will retry up to 15 times
    # to get a valid measurement (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Check if the reading is valid
    if humidity is not None and temperature is not None:
        # print(f'Temperature: {temperature:.1f} degrees')
        # print(f'Humidity: {humidity:.1f}%')
        current_time = time.time()
        if humidity > 50 and (current_time - last_played_time) >= 3600:
            play_sound()
            last_played_time = current_time
    else:
        print('Failed to get reading. Try again!')

# Initialize the last_played_time variable
last_played_time = 0

while True:
    read_dht11()
    time.sleep(2)  # Wait for 2 seconds before taking another reading