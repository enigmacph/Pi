import os
import time
import random
import subprocess

# Path to the folder containing wallpapers
wallpaper_folder = '/home/pi/wallpapers'

# Time interval between wallpaper changes (in seconds)
interval = 300  # 5 minutes

def set_wallpaper(image_path):
    # Command to change the wallpaper in Raspberry Pi OS
    subprocess.run(['pcmanfm', '--set-wallpaper', image_path])

def main():
    while True:
        # Get a list of all image files in the folder
        wallpapers = [f for f in os.listdir(wallpaper_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not wallpapers:
            print("No images found in the specified folder.")
            break
        
        # Randomly choose an image
        selected_wallpaper = random.choice(wallpapers)
        wallpaper_path = os.path.join(wallpaper_folder, selected_wallpaper)
        
        # Set the chosen wallpaper
        set_wallpaper(wallpaper_path)
        
        # Wait for the specified interval before changing the wallpaper again
        time.sleep(interval)

if __name__ == "__main__":
    main()