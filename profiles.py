"""A module for managing player profiles."""
# profiles.py
import datetime
import shutil
import os
import settings
import utils

def _profile_folder(name):
    # nombre limpio (básico): evitar ../ y barras
    clean = str(name).strip().replace("/", "_").replace("\\", "_")
    return os.path.join(settings.PROFILES_DIR, clean)

def profile_exists(name):
    """Verificar si un perfil existe."""
    return os.path.isdir(_profile_folder(name))

def list_profiles():
    """Listar todos los perfiles disponibles."""
    if not os.path.isdir(settings.PROFILES_DIR):
        return []
    entries = []
    for name in os.listdir(settings.PROFILES_DIR):
        p = os.path.join(settings.PROFILES_DIR, name)
        if os.path.isdir(p):
            entries.append(name)
    return sorted(entries)

def create_profile(name):
    """Crear un nuevo perfil."""
    folder = _profile_folder(name)
    os.makedirs(folder, exist_ok=True)
    profile_path = os.path.join(folder, settings.PROFILE_FILENAME)
    # si ya existe, no lo sobreescribimos
    if os.path.exists(profile_path):
        return False
    data = {
        "name": name,
        "created_at": datetime.datetime.utcnow().isoformat()+"Z",
        "highscore": 0,
        "last_score": 0,
        "play_count": 0,
        # extensible: puedes guardar preferencias del usuario aquí
        "prefs": {}
    }
    utils.save_json(profile_path, data)
    return True

def delete_profile(name):
    """Eliminar un perfil existente."""
    folder = _profile_folder(name)
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        return True
    return False

def load_profile(name):
    """Cargar un perfil existente."""
    folder = _profile_folder(name)
    profile_path = os.path.join(folder, settings.PROFILE_FILENAME)
    default = {
        "name": name,
        "created_at": None,
        "highscore": 0,
        "last_score": 0,
        "play_count": 0,
        "prefs": {}
    }
    return utils.load_json(profile_path, default)

def save_profile(name, data):
    """Guardar un perfil existente."""
    folder = _profile_folder(name)
    os.makedirs(folder, exist_ok=True)
    profile_path = os.path.join(folder, settings.PROFILE_FILENAME)
    utils.save_json(profile_path, data)
