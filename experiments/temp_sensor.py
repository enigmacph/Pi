import Adafruit_DHT
import time

# Set sensor type : Options are DHT11, DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO pin where the data pin of DHT11 is connected
pin = 4  # Replace with the GPIO pin number you used (e.g., GPIO4 corresponds to pin 7)

def read_dht11():
    # Try to get a sensor reading. The read_retry method will retry up to 15 times
    # to get a valid measurement (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Check if the reading is valid
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:.1f} degrees')
        print(f'Humidity: {humidity:.1f}%')
    else:
        print('Failed to get reading. Try again!')

if __name__ == '__main__':
    while True:
        read_dht11()
        time.sleep(2)  # Wait for 2 seconds before taking another reading
