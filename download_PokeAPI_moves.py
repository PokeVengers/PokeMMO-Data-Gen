import requests
import json

# Constants
BASE_URL = "https://pokeapi.co/api/v2/move/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "moves-data.json"

def get_all_moves():
    moves = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            moves.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch moves list: HTTP {response.status_code}")
            break

    return [move["name"] for move in moves]

def get_move_data(move_name):
    response = requests.get(f"{BASE_URL}{move_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for move {move_name}")
        return None

def is_move_in_generations_1_to_5(move_data):
    generation_name = move_data.get("generation", {}).get("name", "")
    return generation_name in ["generation-i", "generation-ii", "generation-iii", "generation-iv", "generation-v"]

def process_move_data(raw_data):
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "accuracy": raw_data.get("accuracy"),
        "effect_chance": raw_data.get("effect_chance"),
        "pp": raw_data.get("pp"),
        "priority": raw_data.get("priority"),
        "power": raw_data.get("power"),
        "damage_class": raw_data.get("damage_class", {}).get("name"),
        "type": raw_data.get("type", {}).get("name"),
    }
    return processed_data

def save_moves_to_file(moves, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(moves, file, ensure_ascii=False, indent=4)

def main():
    all_move_names = get_all_moves()
    all_moves = {}

    for move_name in all_move_names:
        move_data = get_move_data(move_name)
        if move_data and is_move_in_generations_1_to_5(move_data):
            processed_data = process_move_data(move_data)
            all_moves[processed_data["name"]] = processed_data

    save_moves_to_file(all_moves, OUTPUT_FILE)

if __name__ == "__main__":
    main()
