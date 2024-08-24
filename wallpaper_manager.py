import os
import random
import subprocess

# Path to the folder containing wallpapers
wallpaper_folder = '/home/pi/wallpapers'

def set_wallpaper(image_path):
    # Set environment variables to access the graphical session
    os.environ['DISPLAY'] = ':0'  # This is typically the display for the Pi's desktop session
    os.environ['XAUTHORITY'] = '/home/pi/.Xauthority'  # Adjust if the user is different
    os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'  # Adjust if the user is different

    # Command to change the wallpaper in Raspberry Pi OS
    subprocess.run(['pcmanfm', '--set-wallpaper', image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Get a list of all image files in the folder
wallpapers = [f for f in os.listdir(wallpaper_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
if not wallpapers:
    print("No images found in the specified folder.")
else:
    # Randomly choose an image
    selected_wallpaper = random.choice(wallpapers)
    wallpaper_path = os.path.join(wallpaper_folder, selected_wallpaper)
    
    # Set the chosen wallpaper
    set_wallpaper(wallpaper_path)