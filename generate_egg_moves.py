import json

DATA_SAVE_PATH = "./data/"
INPUT_FILE = "pokemon-data.json"
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

def can_breed(pokemon1, pokemon2, egg_groups, gender_rates):
    if gender_rates[pokemon1] == -1 and pokemon2 not in [pokemon1, 'ditto']:
        return False
    if gender_rates[pokemon2] == -1 and pokemon1 not in [pokemon2, 'ditto']:
        return False
    return egg_groups[pokemon1].intersection(egg_groups[pokemon2]) and "cannot-breed" not in egg_groups[pokemon1]

def find_breeding_partners(pokemon, all_pokemon, egg_groups, gender_rates):
    return [p for p in all_pokemon if can_breed(pokemon, p, egg_groups, gender_rates)]

# Memoization cache for breeding chains
breeding_chain_cache = {}

def breeding_chain(pokemon, move, all_pokemon, current_chain, visited, egg_groups, gender_rates, depth=0, max_depth=5):
    if pokemon in visited or depth > max_depth:
        return []
    visited.add(pokemon)

    cache_key = (pokemon, move, tuple(current_chain))
    if cache_key in breeding_chain_cache:
        visited.remove(pokemon)
        return breeding_chain_cache[cache_key]

    if 'moves' not in all_pokemon[pokemon]:
        visited.remove(pokemon)
        return []

    if any(m['name'] == move and m['type'] != 'egg_moves' for m in all_pokemon[pokemon]['moves']):
        breeding_chain_cache[cache_key] = [current_chain]
        visited.remove(pokemon)
        return [current_chain]

    chains = []
    for breeder in find_breeding_partners(pokemon, all_pokemon, egg_groups, gender_rates):
        if breeder not in visited:
            chains.extend(breeding_chain(breeder, move, all_pokemon, current_chain + [breeder], visited.copy(), egg_groups, gender_rates, depth + 1, max_depth))

    breeding_chain_cache[cache_key] = chains
    visited.remove(pokemon)
    return chains

def determine_breeding_chains(all_pokemon, egg_moves, egg_groups, gender_rates):
    breeding_chains = {}
    for pokemon, moves in egg_moves.items():
        breeding_chains[pokemon] = {}
        for move in moves:
            breeding_chains[pokemon][move] = breeding_chain(pokemon, move, all_pokemon, [pokemon], set(), egg_groups, gender_rates)
    return breeding_chains

def write_json(data, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    pokemon_data = load_json(INPUT_FILE)

    egg_groups = {pokemon: set(data['egg_groups']) for pokemon, data in pokemon_data.items()}
    gender_rates = {pokemon: data['gender_rate'] for pokemon, data in pokemon_data.items()}

    egg_moves = extract_egg_moves(pokemon_data)
    breeding_chains = determine_breeding_chains(pokemon_data, egg_moves, egg_groups, gender_rates)

    write_json(breeding_chains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
