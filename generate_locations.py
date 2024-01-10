import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
LOCATIONS_FILE = os.path.join(current_dir, "locations.json")
info_directory = os.path.join(current_dir, "dump/info")

# Add your lookup dictionary here
name_change_lookup = {
    'nidoran♀': 'nidoran-f',
    'nidoran♂': 'nidoran-m',
    # Add more name mappings as needed
}

def generate_locations_json(directory):
    # Dictionary to hold all location data
    locations_data = {}

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
                
                # Extracting the location information
                locations_data[pokemon_name] = {'locations': data.get('locations', [])}
    
    # Write the compiled data to locations.json
    with open(LOCATIONS_FILE, 'w', encoding="utf-8") as outfile:
        json.dump(locations_data, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_locations_json(info_directory)
