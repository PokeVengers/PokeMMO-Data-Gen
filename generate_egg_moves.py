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

def can_breed(pokemon1, pokemon2, egg_groups, gender_rates):
    """ Check if two Pokémon can breed based on their egg groups and gender rates. """
    if gender_rates[pokemon1] == -1 and pokemon2 not in [pokemon1, 'ditto']:
        return False
    if gender_rates[pokemon2] == -1 and pokemon1 not in [pokemon2, 'ditto']:
        return False
    return egg_groups[pokemon1].intersection(egg_groups[pokemon2]) and "cannot-breed" not in egg_groups[pokemon1]

def find_breeding_partners(pokemon, all_pokemon, egg_groups, gender_rates):
    """ Find all possible breeding partners for a given Pokémon. """
    return [p for p in all_pokemon if can_breed(pokemon, p, egg_groups, gender_rates)]

# Memoization cache for breeding chains
breeding_chain_cache = {}

def breeding_chain(pokemon, move, all_pokemon, current_chain, visited, depth=0, max_depth=10):
    """ Recursively find breeding chains for a specific move. """
    if pokemon in visited or depth > max_depth:
        return []
    visited.add(pokemon)

    cache_key = (pokemon, move, tuple(current_chain))
    if cache_key in breeding_chain_cache:
        visited.remove(pokemon)  # Remove pokemon from visited before returning
        return breeding_chain_cache[cache_key]

    if 'moves' not in all_pokemon[pokemon] or not any(m['name'] == move and m['type'] != 'egg_moves' for m in all_pokemon[pokemon]['moves']):
        visited.remove(pokemon)
        return []

    chains = []
    for breeder in breeding_partners[pokemon]:
        if breeder not in visited:
            chains.extend(breeding_chain(breeder, move, all_pokemon, current_chain + [breeder], visited, depth + 1, max_depth))

    breeding_chain_cache[cache_key] = chains
    visited.remove(pokemon)
    return chains

def determine_breeding_chains(all_pokemon, egg_moves):
    """ Determine breeding chains for each egg move of each Pokémon. """
    breeding_chains = {}
    for pokemon, moves in egg_moves.items():
        breeding_chains[pokemon] = {}
        for move in moves:
            breeding_chains[pokemon][move] = breeding_chain(pokemon, move, all_pokemon, [pokemon], set(), 0, max_depth=10)
    return breeding_chains

def write_json(data, filename):
    """ Write data to a JSON file. """
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    pokemon_data = load_json(INPUT_FILE)

    egg_groups = {pokemon: set(data['egg_groups']) for pokemon, data in pokemon_data.items()}
    gender_rates = {pokemon: data['gender_rate'] for pokemon, data in pokemon_data.items()}
    global breeding_partners
    breeding_partners = {pokemon: find_breeding_partners(pokemon, pokemon_data, egg_groups, gender_rates) for pokemon in pokemon_data}

    egg_moves = extract_egg_moves(pokemon_data)
    breeding_chains = {pokemon: {move: breeding_chain(pokemon, move, pokemon_data, [pokemon], set()) for move in moves} for pokemon, moves in egg_moves.items()}

    write_json(breeding_chains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
