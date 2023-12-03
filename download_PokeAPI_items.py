import requests
import json

# Constants
BASE_URL = "https://pokeapi.co/api/v2/item/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "item-data.json"

def get_all_items():
    items = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            items.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch items list: HTTP {response.status_code}")
            break

    return [item["name"] for item in items]

def get_item_data(item_name):
    response = requests.get(f"{BASE_URL}{item_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for item {item_name}")
        return None

def process_item_data(raw_data):
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "attributes": [attr["name"] for attr in raw_data.get("attributes", [])],
        "category": raw_data.get("category", {}).get("name"),
        "effect": raw_data.get("effect_entries")[0].get("short_effect") if raw_data.get("effect_entries") else None,
        "sprite": raw_data.get("sprites", {}).get("default")
    }
    return processed_data

def save_items_to_file(items, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def main():
    all_item_names = get_all_items()
    all_items = {}

    for item_name in all_item_names:
        item_data = get_item_data(item_name)
        if item_data:
            processed_data = process_item_data(item_data)
            all_items[processed_data["name"]] = processed_data

    save_items_to_file(all_items, OUTPUT_FILE)

if __name__ == "__main__":
    main()
