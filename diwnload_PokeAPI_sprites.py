import requests
import json
import os

# Base URL for the PokeAPI
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
DATA_SAVE_PATH = "./data/"
SPRITES_FILE = "pokemon-sprites.json"

def get_pokemon_sprites(pokemon_id):
    response = requests.get(POKEMON_BASE_URL + str(pokemon_id))
    if response.status_code == 200:
        pokemon_data = response.json()
        sprites = pokemon_data.get("sprites", {})
        return {
            "id": pokemon_id,
            "name": pokemon_data["name"],
            "sprites": sprites
        }
    return None

def save_sprites_data(sprites_data):
    with open(os.path.join(DATA_SAVE_PATH, SPRITES_FILE), "w", encoding="utf-8") as file:
        json.dump(sprites_data, file, ensure_ascii=False, indent=4)

def main():
    os.makedirs(DATA_SAVE_PATH, exist_ok=True)

    # Fetch the total number of Pokémon
    response = requests.get(POKEMON_BASE_URL)
    total_count = response.json()["count"]

    all_sprites_data = {}
    for i in range(1, total_count + 1):
        pokemon_sprites = get_pokemon_sprites(i)
        if pokemon_sprites:
            all_sprites_data[pokemon_sprites["name"]] = pokemon_sprites

    save_sprites_data(all_sprites_data)

if __name__ == "__main__":
    main()
