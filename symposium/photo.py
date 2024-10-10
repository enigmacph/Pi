import time
import gdown
import os
import subprocess
import random
import pygame

# Set your Google Drive folder URL and the destination folder path on your Raspberry Pi
drive_folder_url = 'https://drive.google.com/drive/u/3/folders/1X2sYmeSK85W6ePTTju_pdw2-E2fwRvzx'  # Replace YOUR_FOLDER_ID with your folder ID
destination_folder = "/home/pi/photos"  # Replace this with the folder path where you want the image to be saved

## Initialize pygame
os.environ["DISPLAY"] = ":0" # set display
pygame.init()
info = pygame.display.Info() # get screen size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)  # Hide the mouse cursor

# Function to extract the file IDs from the folder
def get_file_ids(folder_url):
    # Use gdown to list the contents of the folder
    command = ['gdown', '--folder', folder_url, '--quiet']
    result = subprocess.run(command, capture_output=True, text=True)
    file_ids = []
    
    # Parse the file IDs from the output
    for line in result.stdout.splitlines():
        if line.startswith('file'):
            file_id = line.split()[1]  # Get the file ID from the list output
            file_ids.append(file_id)
    
    return file_ids

# Function to download a random image
def download_random_image(folder_url, destination_folder):
    file_ids = get_file_ids(folder_url)
    
    if not file_ids:
        print("No images found in the folder.")
        return

    # Pick a random file ID
    random_file_id = random.choice(file_ids)
    
    # Set the download URL for the selected file
    file_url = f'https://drive.google.com/uc?id={random_file_id}&export=download'
    
    # Download the image
    output_path = os.path.join(destination_folder, 'photo.jpg')
    
    # Remove the existing 'photo.jpg' if it exists
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Download the new image
    gdown.download(file_url, output_path, quiet=False)
    print(f"Downloaded and saved as {output_path}")

def update_display():
    screen.fill((0,0,0)) # clear screen
    background = pygame.image.load("/home/pi/photos/photo.jpg").convert_alpha()
    screen.blit(background, (0,0))
    pygame.display.flip()

def main():
    while True: 
        # get picture
        print('downloading image')
        download_random_image(drive_folder_url, destination_folder)
        
        # show picture
        print("showing image")
        update_display()

        # wait for some time
        print("sleeping")
        time.sleep(1)

if __name__ == "__main__":
    main()