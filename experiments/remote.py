import time
import pigpio

# Setup GPIO pin for IR sensor
IR_GPIO = 14  # Use the GPIO pin number you connected the IR receiver to

# Initialize pigpio library
pi = pigpio.pi()

# Ensure pigpio daemon is running
if not pi.connected:
    exit()

# Callback function to handle IR signal
def ir_callback(gpio, level, tick):
    if level == 0:  # Signal received (falling edge)
        print(f"Received signal at tick {tick}")

# Set up the callback
cb = pi.callback(IR_GPIO, pigpio.FALLING_EDGE, ir_callback)

try:
    print("Waiting for IR signal...")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up
    cb.cancel()
    pi.stop()