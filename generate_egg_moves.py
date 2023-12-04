import json

DATA_SAVE_PATH = "./data/"
INPUT_FILE = "pokemon-data.json"
OUTPUT_FILE = "egg-moves-data.json"

def load_json(filename):
    """ Load the JSON data from a file. """
    with open(DATA_SAVE_PATH + filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_egg_moves(pokemon_data):
    """ Extract egg moves for each Pokémon. """
    egg_moves = {}
    for pokemon, data in pokemon_data.items():
        if 'moves' in data:
            egg_moves[pokemon] = [move['name'] for move in data['moves'] if move['type'] == 'egg_moves']
        else:
            egg_moves[pokemon] = []
    return egg_moves

def can_breed(pokemon1, pokemon2, all_pokemon):
    """ Check if two Pokémon can breed based on their egg groups and gender rates. """
    if all_pokemon[pokemon1]['gender_rate'] == -1 and pokemon2 not in [pokemon1, 'ditto']:
        return False
    if all_pokemon[pokemon2]['gender_rate'] == -1 and pokemon1 not in [pokemon2, 'ditto']:
        return False
    egg_groups1 = set(all_pokemon[pokemon1]['egg_groups'])
    egg_groups2 = set(all_pokemon[pokemon2]['egg_groups'])
    return egg_groups1.intersection(egg_groups2) and "cannot-breed" not in egg_groups1

def find_breeding_partners(pokemon, all_pokemon):
    """ Find all possible breeding partners for a given Pokémon. """
    return [p for p in all_pokemon if can_breed(pokemon, p, all_pokemon)]

# Memoization cache for breeding chains
breeding_chain_cache = {}

def breeding_chain(pokemon, move, all_pokemon, current_chain, visited=set(), depth=0, max_depth=3):
    """ Recursively find breeding chains for a specific move. """
    # Avoid infinite recursion by checking if we have already visited this pokemon
    if pokemon in visited:
        return []
    visited.add(pokemon)

    # Check if 'moves' key exists
    if 'moves' not in all_pokemon[pokemon]:
        return []

    cache_key = (pokemon, move, tuple(current_chain))
    if cache_key in breeding_chain_cache:
        return breeding_chain_cache[cache_key]

    if move in [m['name'] for m in all_pokemon[pokemon]['moves'] if m['type'] != 'egg_moves']:
        return [current_chain]

    potential_breeders = find_breeding_partners(pokemon, all_pokemon)
    chains = []
    for breeder in potential_breeders:
        if breeder not in visited:
            new_chain = current_chain + [breeder]
            chains.extend(breeding_chain(breeder, move, all_pokemon, new_chain, visited.copy(), depth + 1, max_depth))

    breeding_chain_cache[cache_key] = chains
    return chains

def determine_breeding_chains(all_pokemon, egg_moves):
    """ Determine breeding chains for each egg move of each Pokémon. """
    breeding_chains = {}
    for pokemon, moves in egg_moves.items():
        breeding_chains[pokemon] = {}
        for move in moves:
            breeding_chains[pokemon][move] = breeding_chain(pokemon, move, all_pokemon, [pokemon], set(), 0, max_depth=3)
    return breeding_chains

def write_json(data, filename):
    """ Write data to a JSON file. """
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # Load the original Pokémon data
    pokemon_data = load_json(INPUT_FILE)

    # Extract egg moves for each Pokémon
    egg_moves = extract_egg_moves(pokemon_data)

    # Determine breeding chains for each egg move
    breeding_chains = determine_breeding_chains(pokemon_data, egg_moves)

    # Output the data to a new JSON file
    write_json(breeding_chains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
