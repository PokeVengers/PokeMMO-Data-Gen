import requests
import json

# Base URLs for the PokeAPI
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
ALL_POKEMON_FILE = "pokemon_data.json"

def get_evolution_chain_data(evolution_chain_url):
    response = requests.get(evolution_chain_url)
    if response.status_code == 200:
        evolution_chain_data = response.json()

        # Process the evolution chain to remove nested evolves_to and URLs
        process_evolution_chain(evolution_chain_data['chain'])

        return evolution_chain_data
    return None

def process_evolution_chain(chain):
    if 'evolves_to' in chain:
        # Remove nested evolves_to from each stage
        for evolves_to in chain['evolves_to']:
            process_evolution_chain(evolves_to)  # Recursive call for nested evolves_to

            if 'species' in evolves_to:
                evolves_to['species'] = evolves_to['species']['name']

            evolves_to['evolves_to'] = []  # Clear nested evolves_to

def is_in_first_five_generations(generation_url):
    generation_id = int(generation_url.split('/')[-2])
    return 1 <= generation_id <= 5

def process_egg_groups(egg_groups):
    return [group['name'] for group in egg_groups]

def process_growth_rate(growth_rate):
    return growth_rate['name']

def save_all_data(all_data):
    with open(DATA_SAVE_PATH + ALL_POKEMON_FILE, 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

def main():
    all_pokemon_data = {}

    # Get the total count of Pokémon
    response = requests.get(POKEMON_BASE_URL)
    total_count = response.json()['count']

    # Loop through all Pokémon species
    for i in range(1, total_count + 1):
        species_response = requests.get(POKEMON_SPECIES_URL + str(i))
        if species_response.status_code == 200:
            species_data = species_response.json()

            # Check if the species is in the first five generations
            if not is_in_first_five_generations(species_data['generation']['url']):
                continue  # Skip species not in generations 1-5

            species_data.pop('flavor_text_entries', None)  # Remove unwanted fields
            species_data.pop('genera', None)
            species_data.pop('generation', None)
            species_data.pop('habitat', None)
            species_data.pop('names', None)
            species_data.pop('pal_park_encounters', None)
            species_data.pop('pokedex_numbers', None)
            species_data.pop('color', None)
            species_data.pop('form_descriptions', None)
            species_data.pop('shape', None)
            species_data['egg_groups'] = process_egg_groups(species_data['egg_groups'])
            species_data['growth_rate'] = process_growth_rate(species_data['growth_rate'])

            # Get Evolution Chain Data
            evolution_chain_url = species_data.get('evolution_chain', {}).get('url')
            if evolution_chain_url:
                evolution_chain_data = get_evolution_chain_data(evolution_chain_url)
                species_data['evolution_chain'] = evolution_chain_data

            # Loop through all varieties of the Pokémon species
            for variety in species_data['varieties']:
                pokemon_id = variety['pokemon']['url'].split('/')[-2]  # Extract ID from URL
                pokemon_response = requests.get(POKEMON_BASE_URL + pokemon_id)
                if pokemon_response.status_code == 200:
                    pokemon_data = pokemon_response.json()
                    pokemon_name = pokemon_data['name']
                    
                    pokemon_data.pop('game_indices', None)
                    pokemon_data.pop('location_area_encounters', None)
                    pokemon_data.pop('moves', None)

                    # Remove versions from sprites
                    if 'sprites' in pokemon_data and 'versions' in pokemon_data['sprites']:
                        pokemon_data['sprites'].pop('versions', None)
                        
                    # Remove other from sprites
                    if 'sprites' in pokemon_data and 'other' in pokemon_data['sprites']:
                        pokemon_data['sprites'].pop('other', None)

                    merged_data = {**species_data, **pokemon_data}
                    all_pokemon_data[pokemon_name] = merged_data

    save_all_data(all_pokemon_data)

if __name__ == "__main__":
    main()
