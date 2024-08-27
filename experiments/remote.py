import pigpio
import time

# IR sensor GPIO pin
IR_GPIO = 18  # Replace with the GPIO pin you're using

# Initialize pigpio library
pi = pigpio.pi()

# Ensure pigpio daemon is running
if not pi.connected:
    exit()

# NEC protocol constants
PRE_MARK_MIN = 8500  # Microseconds
PRE_MARK_MAX = 9500  # Microseconds
BIT_MARK_MIN = 400   # Microseconds
BIT_MARK_MAX = 700   # Microseconds
SPACE_ONE_MIN = 1600 # Microseconds
SPACE_ONE_MAX = 2000 # Microseconds
SPACE_ZERO_MIN = 400 # Microseconds
SPACE_ZERO_MAX = 700 # Microseconds

# Variables to hold the IR signal data
last_tick = 0
code = []
bits = []

# Callback function to handle IR signal
def ir_callback(gpio, level, tick):
    global last_tick, code, bits
    
    if level == 0:  # Falling edge
        delta = pigpio.tickDiff(last_tick, tick)
        last_tick = tick

        # Pre-mark: signal start
        if PRE_MARK_MIN <= delta <= PRE_MARK_MAX:
            code = []
            bits = []
        
        # Bit mark: 1 or 0
        elif BIT_MARK_MIN <= delta <= BIT_MARK_MAX:
            code.append(delta)
        
        # Space after bit: 1 or 0
        elif SPACE_ONE_MIN <= delta <= SPACE_ONE_MAX:
            bits.append(1)
        
        elif SPACE_ZERO_MIN <= delta <= SPACE_ZERO_MAX:
            bits.append(0)

        if len(bits) == 32:  # NEC protocol uses 32 bits
            print(f"Received NEC code: {bits_to_hex(bits)}")
