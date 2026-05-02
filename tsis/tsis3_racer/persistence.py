import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "car_color": "BLUE",
    "difficulty": "Normal" # easy, Normal, Hard
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(entries):
    # sort by score descending and keep top 10
    entries.sort(key=lambda x: x.get("score", 0), reverse=True)
    entries = entries[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(entries, f, indent=4)
