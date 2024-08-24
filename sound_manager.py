import soco
import schedule
import time

den = soco.SoCo('192.168.50.198')
bedroom = soco.SoCo('192.168.50.82')
hallway = soco.SoCo('192.168.50.33')

# start 'code red' sequence on the group
def play_sound(filename):
    # Create a new group with den as the coordinator
    try:
        master = den
        den.volume=40
        # bedroom.join(master)
        # bedroom.volume=40
        # hallway.join(master)
        # hallway.volume=40
    except:
        print("Error joining speakers")
    
    try:
        # play alarm sound
        master.play_uri(f"http://192.168.50.252/{filename}.mp3")
    except:
        print("no speakers connected")

# Schedule sounds
# Note that raspberry pi thinks its UK time
schedule.every().day.at("17:00").do(lambda: play_sound("pizzajingle"))
# schedule.every().day.at("10:00").do(lambda: play_sound("gas"))
# schedule.every().day.at("20:00").do(lambda: play_sound("ohyeah"))
# schedule.every().day.at("8:00").do(lambda: play_sound("japan_lul"))
schedule.every().day.at("22:15").do(lambda: play_sound("the_orb"))

# Run the script indefinitely looking for scheduled sounds
while True:
    schedule.run_pending()
    time.sleep(60)