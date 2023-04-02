import soco
import schedule
import time

den = soco.SoCo('192.168.50.198')
bedroom = soco.SoCo('192.168.50.82')
hallway = soco.SoCo('192.168.50.33')

# start 'code red' sequence on the group
def play_sound(filename):
    # Create a new group with den as the coordinator
    master = den
    bedroom.join(master)
    hallway.join(master)
    
    # play alarm sound
    master.play_uri(f"http://192.168.50.252/{filename}.mp3")

# Schedule sounds
schedule.every().day.at("18:00").do(lambda: play_sound("pizzajingle"))
schedule.every().day.at("11:00").do(lambda: play_sound("gas"))
schedule.every().day.at("11:13").do(lambda: play_sound("gas"))

# Run the script indefinitely looking for scheduled sounds
while True:
    schedule.run_pending()
    time.sleep(60)