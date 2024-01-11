import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def run_script(script_path):
    """Runs a Python script at the given path."""
    try:
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        print(f"Script {script_path} executed successfully.")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in script {script_path}: {e}")

# List of scripts to run
scripts_to_run = [
    os.path.join(current_dir, 'generate_obtainable_pokemon.py'),
    os.path.join(current_dir, 'generate_pokemon_moves.py'),
    os.path.join(current_dir, 'generate_locations.py'),
    os.path.join(current_dir, 'download_PokeAPI_pokemon.py'),
    os.path.join(current_dir, 'download_PokeAPI_egg-group.py'),
    os.path.join(current_dir, 'download_PokeAPI_moves.py'),
    os.path.join(current_dir, 'download_PokeAPI_items.py'),
    os.path.join(current_dir, 'generate_egg_moves.py'),
    os.path.join(current_dir, 'download_PokeAPI_abilities.py'),
    os.path.join(current_dir, 'patch_data_files.py'),
    os.path.join(current_dir, 'add_pokemon_to_moves.py'),
    os.path.join(current_dir, 'add_pokemon_to_abilities.py'),
    os.path.join(current_dir, 'add_pvp_to_pokemon.py'),
    os.path.join(current_dir, 'generate_pvp_data.py'),
    os.path.join(current_dir, 'generate_types_data.py'),
    os.path.join(current_dir, 'generate_location_data.py'),
    os.path.join(current_dir, 'generate_obtainable_data.py'),
    os.path.join(current_dir, 'download_PokeAPI_sprites.py')
    ]

for script in scripts_to_run:
    run_script(script)
