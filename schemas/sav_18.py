import zlib
from construct import *

sav18_save_data_schema = Struct(
    "version" / Int32ul,
    "unknown1" / Int32ul,
    "unknown2" / Int32ul,
    "location" / PascalString(Int32ul, "utf8"),
    "runs" / Int32ul,
    "active_meta_points" / Int32ul,
    "active_shrine_points" / Int32ul,
    "grasp" / Int32ul,
    "unknown_int_2" / Int32ul,
    "god_mode_enabled" / Byte,
    "hell_mode_enabled" / Byte,
    "lua_keys" / PrefixedArray(
        Int32ul,
        PascalString(Int32ul, "utf8")
    ),
    "current_map_name" / PascalString(Int32ul, "utf8"),
    "start_next_map" / PascalString(Int32ul, "utf8"),
    "lua_state" / PrefixedArray(Int32ul, Byte)
)

sav18_schema = Struct(
    "signature" / Const(b"SGB1"),
    "checksum_offset" / Tell,
    "checksum" / Padding(4),
    "save_data" / RawCopy(
        sav18_save_data_schema
    ),
    "checksum" / Pointer(
        this.checksum_offset,
        Checksum(
            Int32ul,
            lambda data: zlib.adler32(data, 1),
            this.save_data.data
        )
    )
)
