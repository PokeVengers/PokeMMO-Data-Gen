import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_SAVE_PATH = "./data/"
POKEMON_DATA_FILE = 'pokemon-data.json'
POKEMON_PATCH_FILE = 'patch_pokemon-data.json'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def update_nested_key(data, key_path, value):
    keys = key_path.split('.')
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value

def apply_patch(original_data, patch_data):
    for key, changes in patch_data.items():
        for change_key, value in changes.items():
            if '_add' in change_key:
                list_key = change_key.replace('_add', '')
                if list_key in original_data[key]:
                    original_data[key][list_key].extend(value)
            elif '_remove' in change_key:
                list_key = change_key.replace('_remove', '')
                if list_key in original_data[key]:
                    original_data[key][list_key] = [item for item in original_data[key][list_key] if item not in value]
            elif '.' in change_key:
                update_nested_key(original_data[key], change_key, value)
            else:
                original_data[key][change_key] = value

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():


    pokemon_original_data = load_json(DATA_SAVE_PATH + POKEMON_DATA_FILE)
    pokemon_patch_data = load_json(os.path.join(current_dir, POKEMON_PATCH_FILE))

    apply_patch(pokemon_original_data, pokemon_patch_data)
    save_json(pokemon_original_data, DATA_SAVE_PATH + POKEMON_DATA_FILE)

if __name__ == "__main__":
    main()