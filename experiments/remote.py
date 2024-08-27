#!/usr/bin/python
import evdev
from time import sleep

# returns path of gpio ir receiver device
def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print("Using device", device.path, "\n")
            return device

    print("No device found!")
    sys.exit()

# returns the next InputEvent instance
# blocks until event is available
def get_next_event(dev):
    while(True):
        event = dev.read_one()
        if (event):
            return event

def main():
    device = get_ir_device()

    while True:
        print("Waiting indefinitely for IR signals.  The first received command will be returned.")
        next_event = get_next_event(device)

        print("Received command:", next_event.value, "\n")

if __name__ == "__main__":
    main()