import json
import random

# Function to read predictions from a JSON file
def get_predictions():
    # Provide the path to your JSON file
    path = '/home/pi/Python/Pi/livescreen/market_data_enigma.json'  # Replace this with the actual path

    # Open the JSON file and load its contents
    with open(path, 'r') as file:
        data = json.load(file)  # Load JSON data into a Python dictionary

        # Extract market movements from manifold and metaculus, adding the source key
        market_movements_manifold = [{"source": "manifold", **item} for item in data["manifold"]]
        market_movements_metaculus = [{"source": "metaculus", **item} for item in data["metaculus"]]
        market_movements_kalshi = [{"source": "kalshi", **item} for item in data["kalshi"]]

        # Concatenate results from manifold and metaculus
        market_movements = market_movements_manifold + market_movements_metaculus + market_movements_kalshi

    return market_movements

# Function to pick a random prediction from the JSON data
def pick_random_prediction():
    # Get all the market movements (list of dictionaries)
    all_predictions = get_predictions()

    # Handle case where there are no market movements
    if not all_predictions:
        return ["No market movements available."]

    # Get a random prediction from the list
    prediction = random.choice(all_predictions)

    # Extract the source, question, and probabilities
    source = prediction.get("source", "Unknown source")
    question = prediction.get("question", "Unknown question")
    previous_prob = prediction.get("previous_probability", "Unknown previous probability")
    new_prob = prediction.get("new_probability", "Unknown new probability")

    # Convert probabilities to percentages, if they are numerical
    if isinstance(previous_prob, (int, float)) and isinstance(new_prob, (int, float)):
        # Check if the probabilities are already given as percentages (greater than 1)
        if previous_prob <= 1 and new_prob <= 1:
            previous_prob = f"{previous_prob * 100:.2f}%"
            new_prob = f"{new_prob * 100:.2f}%"
        else:
            # Assume the probabilities are already in percentage form and just format them
            previous_prob = f"{previous_prob:.2f}%"
            new_prob = f"{new_prob:.2f}%"

    # Return a list containing the source, question, and probabilities
    result = [f"Market: {source}", f"{question}", f"{previous_prob} -> {new_prob}"]
    
    return result
