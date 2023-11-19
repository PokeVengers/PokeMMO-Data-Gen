import requests
import json

# Base URLs for the PokeAPI
EGG_GROUP_BASE_URL = "https://pokeapi.co/api/v2/egg-group/"
POKEMON_SPECIES_BASE_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
ALL_EGG_GROUPS_FILE = "egg-groups-data.json"

def save_data(data, file_name):
    with open(DATA_SAVE_PATH + file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def is_in_first_five_generations(species_id):
    response = requests.get(POKEMON_SPECIES_BASE_URL + str(species_id))
    if response.status_code == 200:
        species_data = response.json()
        generation_number = int(species_data['generation']['url'].split('/')[-2])
        return generation_number <= 5
    return False

def process_pokemon_species(pokemon_species_list):
    filtered_species = []
    for species in pokemon_species_list:
        species_id = species['url'].split('/')[-2]
        if is_in_first_five_generations(species_id):
            species.pop('url', None)
            filtered_species.append(species)
    return filtered_species

def get_egg_group_data():
    all_egg_groups = {}

    # Get the total count of egg groups
    response = requests.get(EGG_GROUP_BASE_URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return

    total_egg_groups = response.json()['count']

    # Loop through all egg groups
    for i in range(1, total_egg_groups + 1):
        egg_group_response = requests.get(EGG_GROUP_BASE_URL + str(i))
        if egg_group_response.status_code == 200:
            egg_group_data = egg_group_response.json()

            # Remove the 'name' field
            egg_group_data.pop('names', None)

            # Process and filter pokemon_species for generations 1-5
            if 'pokemon_species' in egg_group_data:
                egg_group_data['pokemon_species'] = process_pokemon_species(egg_group_data['pokemon_species'])

            # Add modified egg group data to all egg groups
            all_egg_groups[f"egg_group_{i}"] = egg_group_data

    return all_egg_groups

def main():
    all_egg_groups_data = get_egg_group_data()
    save_data(all_egg_groups_data, ALL_EGG_GROUPS_FILE)

if __name__ == "__main__":
    main()
