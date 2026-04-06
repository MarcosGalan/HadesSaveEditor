from construct import *

version_identifier_schema = Struct(
    "signature" / Bytes(4),
    "checksum" / Padding(4),
    "version" / Int32ul,
    GreedyBytes,
)
