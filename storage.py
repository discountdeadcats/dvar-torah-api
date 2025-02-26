import json
import os

STORAGE_FILE = "storage.json"

# Load existing data if the file exists
if os.path.exists(STORAGE_FILE):
    with open('storage.json', 'r', encoding='utf-8') as file:
        storage = json.load(file)
else:
    storage = {}  # Start with an empty dictionary

# Ensure counter starts from the highest key
counter = max(map(int, storage.keys()), default=0) if storage else 0

# Function to save the dictionary to a file
def save_storage():
    with open(STORAGE_FILE, "w") as file:
        json.dump(storage, file)
