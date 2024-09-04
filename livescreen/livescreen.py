import pygame
import os
import time
import requests
# import Adafruit_DHT
import cairosvg
import io
import re
import random

import todaydie

import Adafruit_DHT
import time

## Initialize humidity sensor

# Set sensor type : Options are DHT11, DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO pin where the data pin of DHT11 is connected
pin = 4  # Replace with the GPIO pin number you used (e.g., GPIO4 corresponds to pin 7)

## Initialize pygame
os.environ["DISPLAY"] = ":0" # set display
pygame.init()
info = pygame.display.Info() # get screen size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)  # Hide the mouse cursor

# set cool font
font = pygame.font.SysFont("freemono", 26) 

# Sensor setup
# sensor = Adafruit_DHT.DHT22
pin = 4

# Path to wallpaper folder
image_folder = "/home/pi/wallpapers"

def get_next_image():
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'png', 'jpeg'))]
    return os.path.join(image_folder, random.choice(images))

def sanitize_svg(svg_content):
    # Remove or correct the problematic float value
    sanitized_svg = re.sub(r"(\d+\.\d+)(r)", r"\1", svg_content.decode('utf-8'))
    return sanitized_svg.encode('utf-8')

def fetch_weather_widget():
    widget_url = "https://www.yr.no/en/content/2-2618425/meteogram.svg?mode=dark"  # copenhagen dark mode svg
    # widget_url = "https://www.yr.no/en/content/2-2618425/meteogram.svg?"  # not dark mode lol

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
    image_path = get_next_image()
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (info.current_w, info.current_h))
    screen.blit(background, (0, 0))

    # Create a surface for the semi-transparent box
    box_surface = pygame.Surface((info.current_w, info.current_h), pygame.SRCALPHA)

    # RGBA for box behind text
    box_color = (61, 216, 255, 160) 

    # adding box with temperature and humidity
    temp_hum_text = f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%" # Text for temperature and humidity
    temp_hum_surface = font.render(temp_hum_text, True, (255, 255, 255))

    temp_hum_box = temp_hum_surface.get_rect(topleft=(20, info.current_h - 50)) # Temperature and humidity box : dimensions = 464x27
    pygame.draw.rect(box_surface, box_color, temp_hum_box.inflate(20, 20)) # 484x47

    screen.blit(box_surface, (0,0)) # blit box under text onto main screen
    screen.blit(temp_hum_surface, temp_hum_box.topleft) # draw text on top of boxes

    # Today's die
    die = todaydie.die_check() # generate today roll from using date as seed
    die_text = f"Today's die rolled: {die}"
    temp_die_surface = font.render(die_text, True, (255, 255, 255))

    temp_die_box = temp_die_surface.get_rect(topleft=(info.current_h - 1000, info.current_h - 500)) # position of die box
    pygame.draw.rect(box_surface, box_color, temp_die_box.inflate(20, 20))

    screen.blit(box_surface, (0,0))
    screen.blit(temp_die_surface, temp_die_box.topleft)

    # adding weather widget from YR.no
    weather_widget = pygame.image.load(widget_image) # Load and display the weather widget image 

    # crop top and bottom of image
    crop_rect = pygame.Rect(0, 86, 782, 176)  # crop to 782x179 - Define the cropping rectangle (left, top, width, height)
    try: 
        cropped_widget = weather_widget.subsurface(crop_rect).copy() # subsurface crashes script if rect is larger than weather_widget
    except:
        cropped_widget = weather_widget
    
    weather_widget = pygame.transform.scale(cropped_widget, (892, 200))  # Resize
    screen.blit(weather_widget, (info.current_w - 912, info.current_h - 220))  # Position on the screen

    pygame.display.flip()

def main():
    humidity = 0
    temperature = 0
    while True:
        #print("now we are here")
        prev_humidity = humidity
        prev_temperature = temperature

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if type(humidity) != float:
            humidity = prev_humidity
            temperature = prev_temperature

        widget_image = fetch_weather_widget()

        if widget_image:
            update_display(temperature, humidity, widget_image)

        time.sleep(10)  # Change background every 60 seconds

if __name__ == "__main__":
    main()