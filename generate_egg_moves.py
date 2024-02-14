import json
import os

# File paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_SAVE_PATH = "./data/"
DUMP_SAVE_PATH = os.path.join(current_dir, "dump/")
INPUT_FILE = os.path.join(DATA_SAVE_PATH, "pokemon-data.json")
EGG_MOVES_FILE = os.path.join(DUMP_SAVE_PATH, "20230429_egg_moves.txt")
OUTPUT_FILE = os.path.join(DATA_SAVE_PATH, "egg-moves-data.json")

# Load Pokémon data
with open(INPUT_FILE, encoding="utf-8") as f:
    pokemon_data = json.load(f)

# Name change lookup
name_change_lookup = {
    'nidoran♀': 'nidoran-f',
    'nidoran♂': 'nidoran-m',
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr"
    # Add more name mappings as needed
}

# Function to clean up Pokémon names and moves from the line and apply name changes if necessary
def clean_name(name):
    cleaned_name = name.split('(')[0].strip().lower()
    return name_change_lookup.get(cleaned_name, cleaned_name)

# Parse egg moves file and construct the desired structure
egg_moves = {}
with open(EGG_MOVES_FILE, "r", encoding="utf-8") as file:
    for line in file:
        # Splitting line into move and chain of acquisition
        parts = line.strip().split(" <= ")
        pokemon, move = parts[0].split("[")
        pokemon = clean_name(pokemon)  # Clean and lowercase pokemon name, apply name changes
        move = move.rstrip("]")  # Remove closing bracket from move

        chain = [clean_name(part) for part in parts[1].split(", ")]  # Clean each name in the chain, apply name changes
        chain.insert(0, pokemon)  # Insert the current Pokémon at the beginning of the chain

        # Ensure pokemon entry exists
        if pokemon not in egg_moves:
            egg_moves[pokemon] = {}

        # Ensure move entry exists and append the chain
        egg_moves[pokemon].setdefault(move, []).append(chain)

# Save the structured egg moves data to a JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(egg_moves, f, ensure_ascii=False, indent=4)

print("Egg moves data generated successfully.")
