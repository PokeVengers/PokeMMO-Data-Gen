# PokeMMO-Data-generate
This project contains the "build" scripts that generate the data for [PokeMMO-Data](https://github.com/PokeVengers/PokeMMO-Data). The intention is for this repo to be a sub folder in [PokeMMO-Data](https://github.com/PokeVengers/PokeMMO-Data) in order to update the data. Data is built using the data from [PokeAPI](https://pokeapi.co/) as a base. Data formats are kept similar to it as well.

# Contributing
If you would like to contribute, please note that changes should not be made directly in this project. Changes should be made in [PokeMMO-Data-Gen](https://github.com/PokeVengers/PokeMMO-Data-Gen). That project contains the build scripts that generate the data in this repo.

# Reporting Incorrect Data
It is very important that data in this project be as accurate as possible. If you see something that is not correct, please open an issue and it will be addressed as soon as humanly possible.

# Files
- `generate_all_files.py`: This is the main "build" script. If you are trying to generate the data yourself, you should use this file. It will run the other scripts in the needed order.
- `download_PokeAPI_pokemon.py`: This script generates pokemon-data.json.
- `download_PokeAPI_moves.py`: This script generates moves-data.json.
- `download_PokeAPI_egg-group.py`: This script generates egg-groups-data.json.
- `download_PokeAPI_abilities.py`: This script generates abilities-data.json.
- `download_PokeAPI_items.py`: This script generates item-data.json.
- `download_PokeAPI_sprites.py`: This script generates pokemon-sprites.json.
- `add_pokemon_to_abilities.py`: Adds Pokemon to their abilities in abilities-data.json.
- `add_pokemon_to_moves.py`: Adds Pokemon to their moves in moves-data.json.
- `add_pvp_to_pokemon.py`: Adds PVP tiers to the pokemon data.
- `generate_egg_moves.py`: This script generates egg-moves-data.json.
- `generate_location_data.py`: This script generates location-data.json.
- `generate_pvp_data.py`: This script generates pvp-data.json.
- `generate_types_data.py`: This script generates types-data.json.
- `pokemon_moves.json`: This file contains the data for all of the moves that Pokemon can learn. Move changes should be made here.
- `pokemon-pvp-data.json`: This file contains the data for all of the tiers Pokemon are in. Changes to tiers should be done here.
- `locations.json`: This file contains the data for all encounter locations of Pokemon. Location changes should be made here.
- `patch_data_files.py`: This script performs "patches" on the data. This is needed to handle changes that are different from the main series games. Example of the patching format will be below.
- `patch_pokemon-data.json`: This file contains "patches" to the Pokemon data. Things should be added here to make changes to the data if it needs to be different from PokeAPI.
- `patch_move-data.json`: This file contains "patches" to the Move data. Things should be added here to make changes to the data if it needs to be different from PokeAPI.
- `dump\`: This folder contains data exported from the PokeMMO client. This will be used to keep moves and locations up to date.
> Settings -> Utilities -> Dump Moddable Resources -> Pokedex Data

# Patching Format
```json
{
    "bulbasaur": {
        "base_happiness": 60, // Change base happiness
        "new_feature": "example_value", // Add a new feature
        // Update a nested value (evolution_chain -> chain -> evolves_to -> species -> name)
        "evolution_chain.chain.evolves_to.0.species.name": "ivysaur-updated",
        // Add a new move (Note that moves shouldn't be added this way but used as an example.)
        "moves_add": [
            {
                "id": 500,
                "name": "New Move",
                "type": "level",
                "level": 20
            }
        ],
        // Remove an ability
        "abilities_remove": [
            {
                "ability_name": "chlorophyll"
            }
        ]
    }
}
```

# Credits
Credits can be found in [CREDITS.md](https://github.com/PokeVengers/PokeMMO-Data/blob/main/CREDITS.md)