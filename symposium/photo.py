import time
import os
import random
import pygame
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Set your Google Drive folder ID and the destination folder path on your Raspberry Pi
FOLDER_ID = '1X2sYmeSK85W6ePTTju_pdw2-E2fwRvzx'
DESTINATION_FOLDER = "/home/pi/photos"
# DESTINATION_FOLDER = "C:/Users/magnu/OneDrive/Dokumenter/EnigmA/photos/" # testing folder for Magnus

# Initialize Pygame for displaying images
os.environ["DISPLAY"] = ":0"  # Set display for the Raspberry Pi
pygame.init()
info = pygame.display.Info()  # Get screen size
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)  # Hide the mouse cursor

def authenticate_google_drive():
    try:
        # Authenticate using the service account file
        creds = service_account.Credentials.from_service_account_file(
            '/home/pi/Python/Pi/livescreen/symposium/credentials.json', scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_files_in_folder(service, folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        file_ids = [item['id'] for item in items]
        return file_ids
    except HttpError as error:
        print(f"An error occurred while listing files: {error}")
        return []

def download_random_image(service, file_ids, destination_folder):
    if not file_ids:
        print("No images found in the folder.")
        return
    random_file_id = random.choice(file_ids)
    request = service.files().get_media(fileId=random_file_id)
    output_path = os.path.join(destination_folder, 'photo.jpg')

    # Remove the existing 'photo.jpg' if it exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Download the image
    with open(output_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
    print(f"Downloaded image as {output_path}")

def update_display():
    screen.fill((0, 0, 0))  # Clear screen

    # Load the image
    background = pygame.image.load(os.path.join(DESTINATION_FOLDER, 'photo.jpg')).convert_alpha()
    img_width, img_height = background.get_size()
    screen_width, screen_height = screen.get_size()

    # Calculate scaling to fit the screen
    scale_factor = min(screen_width / img_width, screen_height / img_height)

    # Scale the image if it's larger than the screen
    if scale_factor < 1:
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        background = pygame.transform.smoothscale(background, (new_width, new_height))
    else:
        new_width, new_height = img_width, img_height  # No scaling needed

    # Calculate position to center the image
    x_pos = (screen_width - new_width) // 2
    y_pos = (screen_height - new_height) // 2

    # Blit the image to the screen centered
    screen.blit(background, (x_pos, y_pos))
    pygame.display.flip()

def main():
    service = authenticate_google_drive()
    if not service:
        print("Failed to authenticate. Exiting.")
        return
    
    # Get list of image IDs
    file_ids = list_files_in_folder(service, FOLDER_ID)
    if not file_ids:
        print("No files found in Google Drive folder.")
        return

    while True:
        download_random_image(service, file_ids, DESTINATION_FOLDER)
        update_display()
        time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()
