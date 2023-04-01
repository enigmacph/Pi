import soco
import time

den = soco.SoCo('192.168.50.198')
bedroom = soco.SoCo('192.168.50.82')
hallway = soco.SoCo('192.168.50.33')

# Create a new group with den as the coordinator
master = den
bedroom.join(master)
hallway.join(master)

# start 'code red' sequence on the group
def start_code_red():
    master.play_uri("http://192.168.50.252/etminut.mp3")

# Run the script indefinitely, calling start_code_red() every minute
while True:
    start_code_red()
    time.sleep(10)