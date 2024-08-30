import random
import os
from datetime import datetime

# Path to store the roll data
roll_file = "daily_roll.txt"

def read_last_roll():
    if os.path.exists(roll_file):
        with open(roll_file, 'r') as file:
            date_str, roll = file.read().split(',')
            return datetime.strptime(date_str, '%Y-%m-%d').date(), int(roll)
    return None, None

def save_roll(date, roll):
    with open(roll_file, 'w') as file:
        file.write(f"{date},{roll}")

def roll_die():
    return random.randint(1, 20)

def die_check():
    # Check if we've already rolled today
    today = datetime.today().date()
    last_roll_date, last_roll_value = read_last_roll()

    if last_roll_date != today: # Roll the die if we haven't rolled today
        last_roll_value = roll_die() # roll today's D20
        save_roll(today, last_roll_value) # save out today's roll

    return last_roll_value