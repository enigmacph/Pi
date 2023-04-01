import soco
import schedule
import time

den = soco.SoCo('192.168.50.198')
bedroom = soco.SoCo('192.168.50.82')
hallway = soco.SoCo('192.168.50.33')

# start 'code red' sequence on the group
def start_code_red():
    # Create a new group with den as the coordinator
    master = den
    bedroom.join(master)
    hallway.join(master)
    
    # play alarm sound
    master.play_uri("http://192.168.50.252/code_red_alarm.mp3")

# Schedule start_code_red() to run at a certain time every day
schedule.every().day.at("11:00").do(start_code_red)

# Run the script indefinitely, calling start_code_red() every minute
while True:
    schedule.run_pending()
    time.sleep(60)