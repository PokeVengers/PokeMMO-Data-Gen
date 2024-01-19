import json
import concurrent.futures

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

    # Function to check if a species can participate in breeding
    def can_breed(species_name):
        species_egg_groups = list(get_pokemon_egg_groups(species_name, egg_groups_data))
        return 'ditto' not in species_egg_groups and 'cannot-breed' not in species_egg_groups

    # Function to check if a species can learn the move
    def can_learn(species_name):
        return move in extract_egg_moves(all_pokemon).get(species_name, []) or can_learn_move_naturally(species_name, move, all_pokemon)

    # Check for the earliest evolution of the Pokémon
    earliest_pokemon = find_earliest_evolution(pokemon, all_pokemon)

    # Find potential breeding partners within and across egg groups
    for egg_group_info in egg_groups_data.values():
        for species in egg_group_info['pokemon_species']:
            species_name = species['name']
            earliest_species = find_earliest_evolution(species_name, all_pokemon)
            if earliest_species != earliest_pokemon and can_breed(earliest_species) and can_learn(earliest_species):
                if not any(earliest_species in chain for chain in chains):  # Avoid redundancy
                    chains.append([earliest_pokemon, earliest_species])
                    # Limiting to one level of chain breeding to avoid complexity
                    species_egg_groups = list(get_pokemon_egg_groups(earliest_species, egg_groups_data))
                    for secondary_egg_group_info in egg_groups_data.values():
                        for secondary_species in secondary_egg_group_info['pokemon_species']:
                            secondary_species_name = secondary_species['name']
                            earliest_secondary_species = find_earliest_evolution(secondary_species_name, all_pokemon)
                            if earliest_secondary_species != earliest_species and can_breed(earliest_secondary_species) and can_learn(earliest_secondary_species):
                                if not any(earliest_secondary_species in chain for chain in chains):  # Avoid redundancy
                                    chains.append([earliest_pokemon, earliest_species, earliest_secondary_species])

    return chains


def write_json(data, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def process_pokemon(pokemon, moves, pokemon_data, egg_groups_data):
    return {
        move: sorted(
            list(set(map(tuple, find_breeding_chains(pokemon, move, pokemon_data, egg_groups_data)))),
            key=lambda chain: len(chain)
        ) for move in moves
    }

def main():
    pokemon_data = load_json(INPUT_FILE)
    egg_groups_data = load_json(EGG_GROUPS_FILE)
    egg_moves = extract_egg_moves(pokemon_data)

    breeding_chains = {}

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Create and map futures to Pokemon names
        futures = {executor.submit(process_pokemon, pokemon, moves, pokemon_data, egg_groups_data): pokemon for pokemon, moves in egg_moves.items()}
        
        # Collect results from futures
        for future in concurrent.futures.as_completed(futures):
            pokemon = futures[future]
            result = future.result()
            breeding_chains[pokemon] = result

    # Sort the final output alphabetically by Pokémon name
    sorted_breeding_chains = dict(sorted(breeding_chains.items()))

    write_json(sorted_breeding_chains, OUTPUT_FILE)


if __name__ == "__main__":
    main()
