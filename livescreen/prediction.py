import json
import random

# Function to read predictions from a JSON file
def get_predictions():
    # Provide the path to your JSON file
    path = '/home/pi/Python/Pi/livescreen/market_data_enigma.json'  # Replace this with the actual path

    # Open the JSON file and load its contents
    with open(path, 'r') as file:
        data = json.load(file)  # Load JSON data into a Python dictionary

        # Extract only the list of market movements from manifold only
        market_movements = data["manifold"]

    return market_movements

# Function to pick a random prediction from the JSON data
def pick_random_prediction():
    # Get all the market movements (list of dictionaries)
    all_predictions = get_predictions()

    # Handle case where there are no market movements
    if not all_predictions:
        return "No market movements available."

    # Get a random prediction from the list
    prediction = random.choice(all_predictions)

    # Extract question and probabilities
    question = prediction.get("question", "Unknown question")
    previous_prob = prediction.get("previous_probability", "Unknown previous probability")
    new_prob = prediction.get("new_probability", "Unknown new probability")

    # Construct the response with extracted data
    result = f"Question: {question}\nProbability: {previous_prob} -> {new_prob}"
    
    return result


