import requests
import json

# Base URLs for the PokeAPI
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
ALL_POKEMON_FILE = "pokemon-data.json"

def get_evolution_chain_data(evolution_chain_url):
    response = requests.get(evolution_chain_url)
    if response.status_code == 200:
        evolution_chain_data = response.json()
        process_evolution_chain(evolution_chain_data['chain'])
        return evolution_chain_data
    return None

def process_evolution_chain(chain):
    if 'species' in chain:
        # Remove URL from species field
        if 'url' in chain['species']:
            del chain['species']['url']

    if 'evolves_to' in chain:
        for evolves_to in chain['evolves_to']:
            # Process the next level in the evolution chain
            process_evolution_chain(evolves_to)

            # Remove URLs from evolution details
            if 'evolution_details' in evolves_to:
                for detail in evolves_to['evolution_details']:
                    remove_urls(detail)

            # Replace species with just the name, if present
            if 'species' in evolves_to:
                evolves_to['species'] = evolves_to['species']['name']

            evolves_to['evolves_to'] = []

def remove_urls(dictionary):
    for key, value in list(dictionary.items()):
        if isinstance(value, dict):
            if 'url' in value:
                del dictionary[key]['url']  # Remove URL
            else:
                remove_urls(value)  # Recursive call for nested dictionaries

def is_in_first_five_generations(generation_url):
    generation_id = int(generation_url.split('/')[-2])
    return 1 <= generation_id <= 5

def process_egg_groups(egg_groups):
    return [group['name'] for group in egg_groups]

def process_growth_rate(growth_rate):
    return growth_rate['name']

def process_stats(stats):
    return [{'stat_name': stat['stat']['name'], 'base_stat': stat['base_stat']} for stat in stats]

def process_types(types):
    return [type_entry['type']['name'] for type_entry in types]

def process_varieties(varieties):
    return [{'is_default': variety['is_default'], 'name': variety['pokemon']['name']} for variety in varieties]

def process_abilities(abilities):
    return [{'ability_name': ability['ability']['name'], 'is_hidden': ability['is_hidden'], 'slot': ability['slot']} for ability in abilities]

def process_forms(forms):
    return [form['name'] for form in forms]

def save_all_data(all_data):
    with open(DATA_SAVE_PATH + ALL_POKEMON_FILE, 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

def main():
    all_pokemon_data = {}

    response = requests.get(POKEMON_BASE_URL)
    total_count = response.json()['count']

    for i in range(1, total_count + 1):
        species_response = requests.get(POKEMON_SPECIES_URL + str(i))
        if species_response.status_code == 200:
            species_data = species_response.json()

            if not is_in_first_five_generations(species_data['generation']['url']):
                continue

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

            evolution_chain_url = species_data.get('evolution_chain', {}).get('url')
            if evolution_chain_url:
                evolution_chain_data = get_evolution_chain_data(evolution_chain_url)
                species_data['evolution_chain'] = evolution_chain_data

            species_data['varieties'] = process_varieties(species_data['varieties'])

            for variety in species_data['varieties']:
                pokemon_id = variety['name']
                pokemon_response = requests.get(POKEMON_BASE_URL + pokemon_id)
                if pokemon_response.status_code == 200:
                    pokemon_data = pokemon_response.json()
                    pokemon_name = pokemon_data['name']
                    
                    pokemon_data.pop('game_indices', None)
                    pokemon_data.pop('location_area_encounters', None)
                    pokemon_data.pop('moves', None)

                    if 'sprites' in pokemon_data:
                        pokemon_data['sprites'].pop('versions', None)
                        pokemon_data['sprites'].pop('other', None)

                    # Process stats and types
                    if 'stats' in pokemon_data:
                        pokemon_data['stats'] = process_stats(pokemon_data['stats'])
                    if 'types' in pokemon_data:
                        pokemon_data['types'] = process_types(pokemon_data['types'])
                    if 'abilities' in pokemon_data:
                        pokemon_data['abilities'] = process_abilities(pokemon_data['abilities'])
                    if 'forms' in pokemon_data:
                        pokemon_data['forms'] = process_forms(pokemon_data['forms'])

                    merged_data = {**species_data, **pokemon_data}
                    all_pokemon_data[pokemon_name] = merged_data

    save_all_data(all_pokemon_data)

if __name__ == "__main__":
    main()
