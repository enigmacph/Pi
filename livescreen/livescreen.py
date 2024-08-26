import pygame
import os
import time
import requests
# import Adafruit_DHT
import cairosvg
import io
import re

# Initialize pygame
os.environ["DISPLAY"] = ":0"
pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
pygame.mouse.set_visible(False)  # Hide the mouse cursor

# Load fonts
font = pygame.font.Font(None, 36)

# Sensor setup
# sensor = Adafruit_DHT.DHT22
pin = 4

# Path to your images folder
image_folder = "/home/pi/wallpapers"


def get_next_image():
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'png', 'jpeg'))]
    for image in images:
        yield os.path.join(image_folder, image)

image_cycle = get_next_image()

def sanitize_svg(svg_content):
    # Remove or correct the problematic float value
    sanitized_svg = re.sub(r"(\d+\.\d+)(r)", r"\1", svg_content.decode('utf-8'))
    return sanitized_svg.encode('utf-8')

def fetch_weather_widget():
    widget_url = "https://www.yr.no/en/content/2-2618425/meteogram.svg?mode=dark"  # Replace with your specific SVG widget URL
    response = requests.get(widget_url)
    
    if response.status_code == 200:
        # Convert SVG to PNG in memory
        try:
            svg_data = sanitize_svg(response.content)
            # print("GOT TO HERE")
            png_data = cairosvg.svg2png(bytestring=svg_data)
            
            # Load the PNG data into a Pygame surface or return it
            png_image = io.BytesIO(png_data)
            return png_image  # Return a BytesIO object containing the PNG data
        except Exception as e:
            print(f"Error converting SVG to PNG: {e}")
            return None
    else:
        print(f"Error fetching SVG: HTTP {response.status_code}")
        return None

def update_display(temperature, humidity, widget_image):
    screen.fill((0,0,0)) # clear screen

    # Load and display background image
    image_path = next(image_cycle)
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (info.current_w, info.current_h))
    screen.blit(background, (0, 0))

    # Draw semi-transparent boxes behind the text
    box_color = (0, 0, 0, 128)  # RGBA: black with 50% transparency

    # Text for temperature and humidity
    temp_hum_text = f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%"
    temp_hum_surface = font.render(temp_hum_text, True, (255, 255, 255))

    # Temperature and humidity box
    temp_hum_box = temp_hum_surface.get_rect(topleft=(20, info.current_h - 60))
    pygame.draw.rect(screen, box_color, temp_hum_box.inflate(20, 20))

    # draw text on top of boxes 
    screen.blit(temp_hum_surface, temp_hum_box.topleft)

    # Load and display the weather widget image
    weather_widget = pygame.image.load(widget_image)
    weather_widget = pygame.transform.scale(weather_widget, (600, 300))  # Resize as needed
    screen.blit(weather_widget, (info.current_w - 320, info.current_h - 180))  # Position on the screen

    pygame.display.flip()

def main():
    while True:
        # temperature, humidity = read_sensor()
        temperature, humidity = 23, 50

        widget_image = fetch_weather_widget()

        update_display(temperature, humidity, widget_image)
        time.sleep(60)  # Change background every 60 seconds

if __name__ == "__main__":
    main()