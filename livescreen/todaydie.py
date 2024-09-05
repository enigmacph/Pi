import random
from datetime import datetime

def roll_die():
    return random.randint(1, 20)

def die_check():
    # Get today's date and use it as a seed
    today = datetime.today().date()
    seed = int(today.strftime('%Y%m%d'))  # Convert date to a seed (e.g., 20240904 for September 4, 2024)
    
    # Seed the random number generator with today's seed
    random.seed(seed)
    
    # Roll the die
    today_roll = roll_die()

    random.seed() # resets seed for background
    
    return today_roll