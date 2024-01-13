import json
from pathlib import Path


def load_path(filepath):
    full_path = Path(__file__).parent.parent.joinpath(f'shemas/{filepath}')
    print(f"Full path to the file: {full_path}")
    with open(full_path) as file:
        schema = json.load(file)
        return schema

