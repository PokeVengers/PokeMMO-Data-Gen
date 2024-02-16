import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
pvp_data_file = os.path.join(current_dir, "pokemon-pvp-data.json")
info_directory = os.path.join(current_dir, "dump/info")
monsters_file = os.path.join(info_directory, "monsters.json")  # Path to the monsters.json file

# Lookup table for tier name changes
tier_lookup = {
    "Untiered": "UN",  # Example mapping, adjust as necessary
    "Under Used": "UU",
    "Never Used": "NU",
    "Over Used": "OU",
    "Ubers": "UB",
    # Add any additional tier mappings here
}

# Name change lookup, if necessary, based on your previous script example
name_change_lookup = {
    "nidoran♀": "nidoran-f",
    "nidoran♂": "nidoran-m",
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr",
    "shaymin": "shaymin-land",
    "basculin": "basculin-red-striped",
    "wormadam": "wormadam-plant",
    # Add more name mappings as needed
}

def generate_pvp_data_json(filepath):
    pvp_data = {}

    # Open the monsters.json file
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

        for pokemon in data:
            # Using the Pokémon's name in lowercase as the key
            pokemon_name = pokemon["name"].lower()

            # Check if the Pokémon's name needs to be changed
            if pokemon_name in name_change_lookup:
                pokemon_name = name_change_lookup[pokemon_name]

            # Extracting the tier information and handling if it's a list
            tier_info = pokemon.get("tiers", "UN")  # Default to "UN" if tier is not specified
            if isinstance(tier_info, list):
                # Assuming we take the first tier in the list for simplicity
                tier = tier_info[0] if tier_info else "UN"
            else:
                tier = tier_info

            tier = tier_lookup.get(tier, "UN")  # Map tier using the lookup table, default to "UN"

            # Constructing the PvP data
            pvp_data[pokemon_name] = {"pvp": [{"tier": tier}]}

    # Write the compiled PvP data to pokemon-pvp-data.json
    with open(pvp_data_file, "w", encoding="utf-8") as outfile:
        json.dump(pvp_data, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_pvp_data_json(monsters_file)
