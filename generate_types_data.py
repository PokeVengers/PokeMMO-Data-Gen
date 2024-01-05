import json
import os

def read_pokemon_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_types_data(pokemon_data):
    types_data = {}
    for pokemon, data in pokemon_data.items():
        for poke_type in data.get('types', []):
            if poke_type not in types_data:
                types_data[poke_type] = []
            types_data[poke_type].append({"name": pokemon, "id": data["id"]})
    return types_data

def save_types_data(types_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(types_data, file, ensure_ascii=False, indent=4)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    all_pokemon_file = "pokemon-data.json"
    types_file = "types-data.json"

    # Read the existing Pokémon data
    pokemon_data_path = os.path.join(data_save_path, all_pokemon_file)
    pokemon_data = read_pokemon_data(pokemon_data_path)

    # Generate Types data
    types_data = generate_types_data(pokemon_data)

    # Save the Types data to a JSON file
    types_data_path = os.path.join(data_save_path, types_file)
    save_types_data(types_data, types_data_path)

    print(f"Types data saved to {types_data_path}")

if __name__ == "__main__":
    main()
