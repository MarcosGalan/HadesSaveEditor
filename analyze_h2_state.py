import sys
import json
from models.save_file import HadesSaveFile

save_path = '/Users/marcosgalan/Library/Application Support/Supergiant Games/Hades II/Profile1.sav'

try:
    hsf = HadesSaveFile.from_file(save_path)
    state = hsf.lua_state._active_state
    
    # Filter GameState to see what's interesting
    gs = state.get("GameState", {})
    
    analysis = {
        "Resources": gs.get("Resources"),
        "WeaponsUnlocked": gs.get("WeaponsUnlocked"),
        "Flags": gs.get("Flags"),
        "WorkshopTinkerStatus": gs.get("WorkshopTinkerStatus"),
        "WorldLevel": gs.get("WorldLevel"),
        "LifetimeResources": gs.get("LifetimeResources"),
        "CompletedRuns": gs.get("CompletedRuns"),
        "Incantations": gs.get("Incantations"),
        "MetaUpgradeState": gs.get("MetaUpgradeState"), # Arcanas?
        "Gift": gs.get("Gift"),
        "Traits": gs.get("Traits"),
    }
    
    print(json.dumps(analysis, indent=2))
except Exception as e:
    print(f"Error: {e}")
