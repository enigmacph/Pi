import pygame
import os
import time
import re
import random
import numpy as np

import todaydie # today die script
import prediction # get metaculus and manifold predictions
import weather # get yr weather forecast

import Adafruit_DHT
import time

# list of loading sentences
loading_messages = [
    "Honeypotting diplomats and blackmailing them for seed funding...",
    "Synthesizing the perfect algorithm to predict the coffee machine's next breakdown...",
    "Negotiating with the CPU for extra processing power...",
    "Redirecting background radiation to speed up downloads...",
    "Calibrating the sensors to detect extraterrestrial Wi-Fi...",
    "Reconfiguring the air molecules for optimized signal strength...",
    "Persuading the RAM to remember what it forgot...",
    "Scanning nearby devices for spontaneous cooperation...",
    "Fine-tuning the weather predictions with dark magic and machine learning...",
    "Running secret negotiations with nearby IoT devices for faster boot times...",
    "Checking with the NSA if it’s okay to continue...",
    "Harnessing Wi-Fi from the neighbor's router...",
    "Optimizing time travel algorithms to reduce boot lag...",
    "Bribing the CPU with extra voltage for faster responses...",
    "Running background checks on nearby Bluetooth devices...",
    "Convincing electrons to follow the speed limit...",
    "Borrowing spare bandwidth from your fridge...",
    "Aligning magnetic fields for better performance...",
    "Consulting ancient schematics for optimal efficiency...",
    "Extracting meaning from random data spikes...",
    "Negotiating peace between rival bits and bytes...",
    "Adjusting atmospheric conditions for smoother cloud sync...",
    "Calibrating sensors to detect Wi-Fi ghosts...",
    "Soliciting feedback from the air conditioner on network speed...",
    "Optimizing bits for inter-dimensional travel...",
    "Running a simulated conversation with the router for better signal...",
    "Consulting a higher AI on the meaning of lag...",
    "Recalibrating the quantum flux capacitor...",
    "Diverting unused electrons to the graphics card...",
    "Running diagnostics on virtual memory after last night’s data party...",
    "Recruiting additional processes from alternate timelines...",
    "Enabling top-secret hyper-threading mode...",
    "Attempting to decode the encrypted language of plants...",
    "Summoning extra bandwidth from an unknown realm...",
    "Running anti-lag algorithms powered by hope and optimism...",
    "Analyzing Wi-Fi signal for signs of sentient life...",
    "Engaging in a staring contest with the CPU—stand by...",
    "Redirecting excess processing power to world domination...",
    "Talking your router through some trust issues...",
    "Running a background check on the incoming data...",
    "Optimizing the speed of light for faster boot times...",
    "Scouting the local network for rogue devices...",
    "Optimizing packet delivery with caffeine-fueled algorithms...",
    "Rewriting local laws of physics to favor faster connections...",
    "Generating random but believable excuses for the delay...",
    "Fine-tuning quantum fluctuations for peak performance...",
    "Running deep scans for hidden performance bugs...",
    "Outsourcing computation to a highly skilled ant colony...",
    "Negotiating a ceasefire between competing processes...",
    "Running an audit of system processes... none were harmed (yet)...",
    "Gently persuading stubborn packets to cross the network...",
    "Unlocking the secrets of quantum entanglement for faster load times...",
    "Bribing the power supply for a little extra juice...",
    "Consulting the weather satellite for boot-time optimization...",
    "Recruiting a squirrel to speed up background processes...",
    "Optimizing airflow around the CPU for cooler thoughts...",
    "Convincing the hard drive to forget embarrassing files...",
    "Redirecting solar flares for a faster data sync...",
    "Running an internal investigation into lost packets...",
    "Engaging stealth mode to quietly finish loading...",
    "Teaching the GPU the meaning of humility before finalizing load..."
]

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

def update_display(temperature, humidity, weather_widget, overlay_image):
    screen.fill((0,0,0)) # clear screen
    
    # load background image
    image_path = get_next_image()
    background = pygame.image.load(image_path).convert_alpha()
    background = pygame.transform.scale(background, (info.current_w, info.current_h))

    # screen blending mode 
    background_array = pygame.surfarray.pixels3d(background).astype(np.uint16)
    overlay_array = pygame.surfarray.pixels3d(overlay_image).astype(np.uint16)

    screen_blend_array = 255 - ((255 - background_array) * (255 - overlay_array) // 255)
    blended_surface = pygame.surfarray.make_surface(screen_blend_array.astype(np.uint8))
    blended_surface.set_alpha(230) # 230 = 90% of 255
    screen.blit(blended_surface, (0, 0))
    
    # Create a surface for the semi-transparent box
    box_surface = pygame.Surface((info.current_w, info.current_h), pygame.SRCALPHA)

    # RGBA for box behind text
    box_color = (61, 216, 255, 160) 

    # adding box with temperature and humidity
    temp_hum_text = f"Temp: {temperature}°C  Humidity: {humidity}%" # Text for temperature and humidity
    temp_hum_surface = font.render(temp_hum_text, True, (255, 255, 255))

    temp_hum_box = temp_hum_surface.get_rect(topleft=(400, info.current_h - 40)) # Temperature and humidity box : dimensions = 464x27
    pygame.draw.rect(box_surface, box_color, temp_hum_box.inflate(20, 20)) # 484x47

    # Today's die text and box
    die = todaydie.die_check() # generate today roll from using date as seed
    die_text = f"Today's die roll: {die}"
    die_surface = font.render(die_text, True, (255, 255, 255))

    die_box = die_surface.get_rect(topleft=(10, info.current_h - 40)) # position of die box
    pygame.draw.rect(box_surface, box_color, die_box.inflate(20, 20))

    # getting prediction market result
    current_prediction_text = prediction.pick_random_prediction()

    if len(current_prediction_text) > 1: # if the json with markets is empty then the list will only be 1 element long
        prediction_market_text = current_prediction_text[0]
        prediction_question_text = current_prediction_text[1]
        prediction_question_text = re.sub(r'[^\u0000-\uFFFF]', '', prediction_question_text) # remove emojis from prediction questions
        prediction_percent_text = current_prediction_text[2]
    else:
        prediction_market_text = ""
        prediction_question_text = "no market updates since yesterday"
        prediction_percent_text = ""
    
    # adding market
    prediction_m_surface = font.render(prediction_market_text, True, (255, 255, 255))
    prediction_m_box = prediction_m_surface.get_rect(topleft=(10, 10)) # upper left hand corner
    pygame.draw.rect(box_surface, box_color, prediction_m_box).inflate(20, 20)

    # adding question
    prediction_q_surface = font.render(prediction_question_text, True, (255, 255, 255))
    prediction_q_box = prediction_q_surface.get_rect(topleft=(10, 45)) # upper left hand corner
    pygame.draw.rect(box_surface, box_color, prediction_q_box).inflate(20, 20)

    # adding percent
    prediction_p_surface = font.render(prediction_percent_text, True, (255, 255, 255))
    prediction_p_box = prediction_p_surface.get_rect(topleft=(10, 80)) # upper left hand corner
    pygame.draw.rect(box_surface, box_color, prediction_p_box).inflate(20, 20)

    # add box and text
    # screen.blit(box_surface, (0,0)) # this draws boxes for both temp and hum, and die roll
    screen.blit(temp_hum_surface, temp_hum_box.topleft) # draw temp and hum text
    screen.blit(die_surface, die_box.topleft) # draw die roll text
    screen.blit(prediction_m_surface, prediction_m_box.topleft) # add prediction market
    screen.blit(prediction_q_surface, prediction_q_box.topleft) # add prediction question
    screen.blit(prediction_p_surface, prediction_p_box.topleft) # add prediction percent

    # today die image
    die_image_path = "/home/pi/Python/Pi/livescreen/d20.png"
    die_image = pygame.image.load(die_image_path)
    die_image = pygame.transform.scale(die_image, (150, 150)) # resize from 400x400 to 150x150
    die_image.set_alpha(230) # 230 = 90% of 255
    screen.blit(die_image, (0, info.current_h - 185)) # position of die image

    # weather_widget = weather_widget

    # crop top and bottom of image
    crop_rect = pygame.Rect(0, 86, 782, 176)  # crop to 782x179 - Define the cropping rectangle (left, top, width, height)
    try: 
        cropped_widget = weather_widget.subsurface(crop_rect).copy() # subsurface crashes script if rect is larger than weather_widget
    except:
        cropped_widget = weather_widget
    
    weather_widget = pygame.transform.scale(cropped_widget, (892, 200))  # Resize
    screen.blit(weather_widget, (info.current_w - 902, info.current_h - 210))  # Position on the screen

    pygame.display.flip()

def main():
    first_run = True
    humidity = 0
    temperature = 0

    # control how often elements update
    weather_update_interval = 3600 # only needs to update every hour
    last_weather_update = time.time() 

    while True:
        if first_run:
            screen.fill((0,0,0)) # clear screen
            loader1_surface = font.render("initializing the Orb of Truth...", True, (255, 255, 255))
            screen.blit(loader1_surface, (5, 5))
            loader2_surface = font.render("getting temperature and humidity...", True, (255, 255, 255))
            screen.blit(loader2_surface, (5, 35))
            pygame.display.flip()

        prev_humidity = humidity
        prev_temperature = temperature

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if type(humidity) != float:
            humidity = prev_humidity
            temperature = prev_temperature
        
        if first_run:
            loader3_surface = font.render("getting weather forecast...", True, (255, 255, 255))
            screen.blit(loader3_surface, (5, 65))
            pygame.display.update()
            widget_image = weather.fetch_weather_widget()
            weather_widget = pygame.image.load(widget_image).convert_alpha()
            # if weather_widget: 
            #     print("got first weather widget")
        
        # get weather forecast
        current_time = time.time()
        if current_time - last_weather_update > weather_update_interval:
            try:
                widget_image = weather.fetch_weather_widget()
                weather_widget = pygame.image.load(widget_image).convert_alpha()
                last_weather_update = current_time
            except Exception as e:
                print(e)
            # print("updated weather forecast")

        if first_run:
            lul = random.choice(loading_messages)
            loader3_surface = font.render(lul, True, (255, 255, 255))
            screen.blit(loader3_surface, (5, 95))
            pygame.display.update()
            
            overlay_path = "/home/pi/Python/Pi/livescreen/overlay.png"
            overlay_image = pygame.image.load(overlay_path) # 1920x1080

        # update screen
        if widget_image:
            update_display(temperature, humidity, weather_widget, overlay_image)

        first_run = False
        time.sleep(20)  # Change background every 20 seconds

if __name__ == "__main__":
    main()