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
    return pokemon in all_pokemon and 'moves' in all_pokemon[pokemon] and any(m['name'] == move and m['type'] != 'egg_moves' for m in all_pokemon[pokemon]['moves'])

def find_earliest_evolution(pokemon, all_pokemon):
    """Finds the earliest evolution of a given pokemon if it exists."""
    for p, data in all_pokemon.items():
        evolution_chain = data.get("evolution_chain", {}).get("chain", {})
        while evolution_chain:
            if evolution_chain.get("species", {}).get("name") == pokemon:
                return p  # Returns the earliest evolution
            evolves_to = evolution_chain.get("evolves_to", [])
            if not evolves_to:  # Check if the evolves_to list is empty
                break  # Exit the loop if there are no further evolutions
            evolution_chain = evolves_to[0]
    return pokemon


def find_breeding_chains(pokemon, move, all_pokemon, egg_groups_data):
    chains = []
    pokemon_egg_groups = list(get_pokemon_egg_groups(pokemon, egg_groups_data))

    # Check for the earliest evolution of the Pokémon
    earliest_pokemon = find_earliest_evolution(pokemon, all_pokemon)
    
    for egg_group_key, egg_group_info in egg_groups_data.items():
        if egg_group_info['name'] in pokemon_egg_groups:
            for species in egg_group_info['pokemon_species']:
                species_name = species['name']
                earliest_species = find_earliest_evolution(species_name, all_pokemon)
                if earliest_species != earliest_pokemon and earliest_species in all_pokemon and can_learn_move_naturally(earliest_species, move, all_pokemon):
                    chains.append([earliest_pokemon, earliest_species])

    if len(pokemon_egg_groups) > 1:
        for egg_group_key, egg_group_info in egg_groups_data.items():
            if egg_group_info['name'] in pokemon_egg_groups:
                for species in egg_group_info['pokemon_species']:
                    species_name = species['name']
                    earliest_species = find_earliest_evolution(species_name, all_pokemon)
                    if earliest_species != earliest_pokemon and earliest_species in all_pokemon:
                        species_egg_groups = list(get_pokemon_egg_groups(earliest_species, egg_groups_data))
                        for secondary_egg_group_key, secondary_egg_group_info in egg_groups_data.items():
                            if secondary_egg_group_info['name'] in species_egg_groups and secondary_egg_group_info['name'] != egg_group_info['name']:
                                for secondary_species in secondary_egg_group_info['pokemon_species']:
                                    secondary_species_name = secondary_species['name']
                                    earliest_secondary_species = find_earliest_evolution(secondary_species_name, all_pokemon)
                                    if earliest_secondary_species != earliest_species and earliest_secondary_species in all_pokemon and can_learn_move_naturally(earliest_secondary_species, move, all_pokemon):
                                        chains.append([earliest_pokemon, earliest_species, earliest_secondary_species])

    return chains

def write_json(data, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    pokemon_data = load_json(INPUT_FILE)
    egg_groups_data = load_json(EGG_GROUPS_FILE)
    egg_moves = extract_egg_moves(pokemon_data)

    breeding_chains = {}
    for pokemon, moves in egg_moves.items():
        breeding_chains[pokemon] = {
            move: sorted(
                list(set(map(tuple, find_breeding_chains(pokemon, move, pokemon_data, egg_groups_data)))),
                key=lambda chain: len(chain)
            ) for move in moves
        }

    write_json(breeding_chains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
