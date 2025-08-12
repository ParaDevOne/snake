# utils.py
import random
import settings
import json
import os

def random_free_cell(occupied, extra_forbidden=None):
    occupied_set = set(occupied)
    extra = set(extra_forbidden or [])
    free = [ (x, y)
             for x in range(settings.COLUMNS)
             for y in range(settings.ROWS)
             if (x, y) not in occupied_set and (x, y) not in extra ]
    return random.choice(free) if free else None

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path, obj):
    try:
        # asegurar que la carpeta existe
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f)
    except Exception as e:
        print("No se pudo salvar:", e)
