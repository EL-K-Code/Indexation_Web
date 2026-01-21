from pathlib import Path
import json

def load_all_json_from_dir(directory):
    indexes = {}
    for path in Path(directory).glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            indexes[path.name] = json.load(f)
    return indexes
