from typing import List, Optional

import lz4.block

from models.lua_state import LuaState
from models.raw_save_file import RawSaveFile

# Version 16 stores the lua_state as an LZ4 block-compressed blob.
# The maximum uncompressed buffer size used by the game.
_SAV16_UNCOMPRESSED_SIZE = 9388032


class HadesSaveFile:
    def __init__(
            self,
            version: int,
            location: str,
            runs: int,
            active_meta_points: int,
            active_shrine_points: int,
            god_mode_enabled: bool,
            hell_mode_enabled: bool,
            lua_keys: List[str],
            current_map_name: str,
            start_next_map: str,
            lua_state: LuaState,
            raw_save_file: Optional[RawSaveFile] = None
    ):
        self.version = version
        self.location = location
        self.runs = runs
        self.active_meta_points = active_meta_points
        self.active_shrine_points = active_shrine_points 
        self.god_mode_enabled = god_mode_enabled
        self.hell_mode_enabled = hell_mode_enabled
        self.lua_keys = lua_keys
        self.current_map_name = current_map_name
        self.start_next_map = start_next_map
        self.lua_state = lua_state

        # Unusued, for debugging
        self.raw_save_file = raw_save_file

    @classmethod
    def from_file(cls, path):
        raw_save_file = RawSaveFile.from_file(path)
        lua_state_bytes = bytes(raw_save_file.lua_state_bytes)
        if raw_save_file.version == 16:
            lua_state_bytes = lz4.block.decompress(
                lua_state_bytes,
                uncompressed_size=_SAV16_UNCOMPRESSED_SIZE
            )
        lua_state = LuaState.from_bytes(lua_state_bytes)

        # Unused, for debugging
        lua_state.raw_save_file = raw_save_file

        return HadesSaveFile(
            version=raw_save_file.version,
            location=raw_save_file.save_data['location'],
            runs=raw_save_file.save_data['runs'],
            active_meta_points=raw_save_file.save_data['active_meta_points'],
            active_shrine_points=raw_save_file.save_data['active_shrine_points'],
            god_mode_enabled=raw_save_file.save_data['god_mode_enabled'],
            hell_mode_enabled=raw_save_file.save_data['hell_mode_enabled'],
            lua_keys=raw_save_file.save_data['lua_keys'],
            current_map_name=raw_save_file.save_data['current_map_name'],
            start_next_map=raw_save_file.save_data['start_next_map'],
            lua_state=lua_state,
            raw_save_file=raw_save_file
        )

    def to_file(self, path):
        if self.version in (14, 16):
            lua_state_bytes = self.lua_state.to_bytes()
            if self.version == 16:
                lua_state_bytes = lz4.block.compress(
                    lua_state_bytes,
                    store_size=False
                )
            save_data = {
                'version': self.version,
                'location': self.location,
                'runs': self.runs,
                'active_meta_points': self.active_meta_points,
                'active_shrine_points': self.active_shrine_points,
                'god_mode_enabled': self.god_mode_enabled,
                'hell_mode_enabled': self.hell_mode_enabled,
                'lua_keys': self.lua_keys,
                'current_map_name': self.current_map_name,
                'start_next_map': self.start_next_map,
                'lua_state': lua_state_bytes,
            }
            if self.version == 16:
                if self.raw_save_file and 'unknown1' in self.raw_save_file.save_data:
                    save_data['unknown1'] = self.raw_save_file.save_data['unknown1']
                    save_data['unknown2'] = self.raw_save_file.save_data['unknown2']
                else:
                    save_data['unknown1'] = 0
                    save_data['unknown2'] = 0
                    
            RawSaveFile(
                version=self.version,
                save_data=save_data
            ).to_file(path)
        else:
            raise Exception(f"Unsupported version {self.version}")
