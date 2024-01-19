import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
OBTAINABLE_FILE = os.path.join(current_dir, "obtainable_pokemon.json")
info_directory = os.path.join(current_dir, "dump/info")

# Add your lookup dictionary here for renaming pokemon if needed
name_change_lookup = {
    'nidoran♀': 'nidoran-f',
    'nidoran♂': 'nidoran-m',
    "farfetch'd" : "farfetchd",
    "mr. mime" : "mr-mime",
    "mime jr." : "mime-jr"
    # Add more name mappings as needed
}

def generate_obtainable_json(directory):
    # Dictionary to hold all obtainable data
    obtainable_data = {}

    # Walk through all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding="utf-8") as file:
                data = json.load(file)
                # Using the Pokémon's name in lowercase as the key
                pokemon_name = data['name'].lower()

                # Check if the Pokémon's name needs to be changed
                if pokemon_name in name_change_lookup:
                    pokemon_name = name_change_lookup[pokemon_name]

                # Creating a dictionary with the 'obtainable' key
                obtainable_info = {"obtainable": data.get('obtainable', False)}

                # Assigning the dictionary to the Pokémon name key
                obtainable_data[pokemon_name] = obtainable_info

    # Write the compiled data to obtainable_pokemon.json
    with open(OBTAINABLE_FILE, 'w', encoding="utf-8") as outfile:
        json.dump(obtainable_data, outfile, ensure_ascii=False, indent=4)

# Assuming the script is run in the directory containing 'dump' folder
if __name__ == "__main__":
    generate_obtainable_json(info_directory)
