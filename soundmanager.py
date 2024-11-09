# let's make sounds man
import soco
import schedule
import time

den = soco.SoCo('192.168.50.198')
bedroom = soco.SoCo('192.168.50.33')
# hallway = soco.SoCo('192.168.50.33')

# start 'code red' sequence on the group
def play_sound(filename):
    # Create a new group with den as the coordinator
    try:
        master = den
        den.volume=40
        bedroom.join(master)
        bedroom.volume=40
        hallway.join(master)
        hallway.volume=40
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
schedule.every().day.at("11:00").do(lambda: play_sound("Bells"))
schedule.every().monday.at("10:00").do(lambda: play_sound("gas"))
schedule.every().monday.at("16:00").do(lambda: play_sound("ohyeah"))
schedule.every().wednesday.at("12:00").do(lambda: play_sound("japan_lul"))
schedule.every().friday.at("19:00").do(lambda: play_sound("the_orb"))

# Run the script indefinitely looking for scheduled sounds
while True:
    schedule.run_pending()
    time.sleep(60)