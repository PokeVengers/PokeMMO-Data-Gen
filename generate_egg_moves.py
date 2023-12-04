import json

DATA_SAVE_PATH = "./data/"
INPUT_FILE = "pokemon-data.json"
EGG_GROUPS_FILE = "egg-groups-data.json"
OUTPUT_FILE = "egg-moves-data.json"

def load_json(filename):
    with open(DATA_SAVE_PATH + filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_egg_moves(pokemon_data):
    egg_moves = {}
    for pokemon, data in pokemon_data.items():
        if 'moves' in data:
            egg_moves[pokemon] = [move['name'] for move in data['moves'] if move['type'] == 'egg_moves']
        else:
            egg_moves[pokemon] = []
    return egg_moves

def get_pokemon_egg_groups(pokemon, egg_groups_data):
    for egg_group_key, egg_group_info in egg_groups_data.items():
        if any(species['name'] == pokemon for species in egg_group_info['pokemon_species']):
            yield egg_group_info['name']

def can_learn_move_naturally(pokemon, move, all_pokemon):
    return 'moves' in all_pokemon[pokemon] and any(m['name'] == move and m['type'] != 'egg_moves' for m in all_pokemon[pokemon]['moves'])

def find_breeding_chains(pokemon, move, all_pokemon, egg_groups_data):
    chains = []
    pokemon_egg_groups = list(get_pokemon_egg_groups(pokemon, egg_groups_data))
    
    for egg_group_key, egg_group_info in egg_groups_data.items():
        if egg_group_info['name'] in pokemon_egg_groups:
            for species in egg_group_info['pokemon_species']:
                species_name = species['name']
                if species_name != pokemon and can_learn_move_naturally(species_name, move, all_pokemon):
                    chains.append([pokemon, species_name])

    # Check for second-level breeding chains if the Pokémon belongs to multiple egg groups
    if len(pokemon_egg_groups) > 1:
        for egg_group_key, egg_group_info in egg_groups_data.items():
            if egg_group_info['name'] in pokemon_egg_groups:
                for species in egg_group_info['pokemon_species']:
                    species_name = species['name']
                    if species_name != pokemon:
                        species_egg_groups = list(get_pokemon_egg_groups(species_name, egg_groups_data))
                        for secondary_egg_group_key, secondary_egg_group_info in egg_groups_data.items():
                            if secondary_egg_group_info['name'] in species_egg_groups and secondary_egg_group_info['name'] != egg_group_info['name']:
                                for secondary_species in secondary_egg_group_info['pokemon_species']:
                                    secondary_species_name = secondary_species['name']
                                    if secondary_species_name != species_name and can_learn_move_naturally(secondary_species_name, move, all_pokemon):
                                        chains.append([pokemon, species_name, secondary_species_name])

    return chains
def main():
    pokemon_data = load_json(INPUT_FILE)
    egg_groups_data = load_json(EGG_GROUPS_FILE)
    egg_moves = extract_egg_moves(pokemon_data)

    breeding_chains = {}
    for pokemon, moves in egg_moves.items():
        breeding_chains[pokemon] = {move: find_breeding_chains(pokemon, move, pokemon_data, egg_groups_data) for move in moves}

    write_json(breeding_chains, OUTPUT_FILE)

def write_json(data, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
