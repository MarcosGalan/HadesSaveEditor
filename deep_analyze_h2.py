import sys
import json
from models.save_file import HadesSaveFile

save_path = '/Users/marcosgalan/Library/Application Support/Supergiant Games/Hades II/Profile1.sav'

try:
    hsf = HadesSaveFile.from_file(save_path)
    state = hsf.lua_state._active_state
    gs = state.get("GameState", {})
    
    analysis = {
        "Resources": gs.get("Resources"),
        "LifetimeResources": gs.get("LifetimeResources"),
        "WeaponsUnlocked": gs.get("WeaponsUnlocked"),
        "WeaponUnlocks": gs.get("WeaponUnlocks"),
        "Flags": gs.get("Flags"),
        "CompletedRuns": gs.get("CompletedRuns"),
        "RoomsVisited": gs.get("RoomsVisited"),
    }
    
    print(json.dumps(analysis, indent=2))
except Exception as e:
    print(f"Error: {e}")
