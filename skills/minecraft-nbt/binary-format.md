See also: [basics.md](basics.md) for fundamentals, [snbt.md](snbt.md) for SNBT text format

# Binary NBT Format

The NBT binary format is a serialization of a tree of typed, named tags. Files are typically GZip-compressed in Java Edition; Bedrock Edition uses little-endian encoding and may be uncompressed.

## Tag Structure

Every tag (except TAG_End) has this structure:

```
[tag_type: 1 byte, unsigned]
[name_length: 2 bytes, unsigned, big-endian (Java) / little-endian (Bedrock)]
[name: name_length bytes, UTF-8 encoded]
[payload: variable, depends on tag type]
```

**TAG_End** is special: it has NO name section. Just a single `0x00` byte.

## Complete Tag Reference

### TAG_End (ID: 0, 0x00)
- **Payload**: None
- **Description**: Marks end of a compound tag. Also used for empty list content type in newer versions.
- **Bytes**: `00`

### TAG_Byte (ID: 1, 0x01)
- **Payload**: 1 byte, signed
- **Range**: -128 to 127
- **Bytes**: `01 [name] [1 byte value]`

### TAG_Short (ID: 2, 0x02)
- **Payload**: 2 bytes, signed, big-endian
- **Range**: -32,768 to 32,767
- **Bytes**: `02 [name] [2 bytes]`

### TAG_Int (ID: 3, 0x03)
- **Payload**: 4 bytes, signed, big-endian
- **Range**: -2,147,483,648 to 2,147,483,647
- **Bytes**: `03 [name] [4 bytes]`

### TAG_Long (ID: 4, 0x04)
- **Payload**: 8 bytes, signed, big-endian
- **Range**: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- **Bytes**: `04 [name] [8 bytes]`

### TAG_Float (ID: 5, 0x05)
- **Payload**: 4 bytes, IEEE 754-2008 binary32, signed, big-endian
- **Range**: ~±3.4E38 (precision varies)
- **Bytes**: `05 [name] [4 bytes]`

### TAG_Double (ID: 6, 0x06)
- **Payload**: 8 bytes, IEEE 754-2008 binary64, signed, big-endian
- **Range**: ~±1.79E308 (precision varies)
- **Bytes**: `06 [name] [8 bytes]`

### TAG_Byte_Array (ID: 7, 0x07)
- **Payload**: 4-byte signed int (big-endian) for size, then `size` bytes
- **Max elements**: ~2,147,483,639 to 2,147,483,647 (JVM-dependent)
- **Bytes**: `07 [name] [size: 4B] [size * byte]`

### TAG_String (ID: 8, 0x08)
- **Payload**: 2-byte **unsigned** short (big-endian) for byte length, then UTF-8 bytes (NOT null-terminated)
- **Max length**: 65,535 bytes
- **Encoding**: Modified UTF-8 (as used by Java)
- **Bytes**: `08 [name] [length: 2B unsigned] [length * UTF-8 bytes]`

### TAG_List (ID: 9, 0x09)
- **Payload**: 1-byte tag ID of list contents, 4-byte signed int (big-endian) for size, then `size` payloads (NO tag IDs or names for each element)
- **Max elements**: 2,147,483,639 (ArrayList limit)
- **Nesting limit**: 512 levels deep
- **Bytes**: `09 [name] [content_tag_id: 1B] [size: 4B] [size * payloads_without_id_or_name]`

### TAG_Compound (ID: 10, 0x0A)
- **Payload**: Sequence of fully-formed tags (each with type ID, name, and payload), terminated by TAG_End
- **No duplicate names** allowed within a compound
- **Nesting limit**: 512 levels deep
- **Bytes**: `0A [name] [tag][tag]...[tag] 00`

### TAG_Int_Array (ID: 11, 0x0B)
- **Payload**: 4-byte signed int (big-endian) for size, then `size` TAG_Int payloads (4 bytes each)
- **Max elements**: ~2,147,483,639 to 2,147,483,647 (JVM-dependent)
- **Bytes**: `0B [name] [size: 4B] [size * 4B]`

### TAG_Long_Array (ID: 12, 0x0C)
- **Payload**: 4-byte signed int (big-endian) for size, then `size` TAG_Long payloads (8 bytes each)
- **Max elements**: ~2,147,483,639 to 2,147,483,647 (JVM-dependent)
- **Bytes**: `0C [name] [size: 4B] [size * 8B]`

## Endianness

| Edition | Multi-byte number endianness |
|---------|------------------------------|
| Java Edition | Big-endian |
| Bedrock Edition | Little-endian |

This applies to: tag name length prefix, string length prefix, list/array size, and all numeric tag payloads. Yes, this means the same NBT file has different binary layouts on Java vs Bedrock.

## File-Level Structure

### Java Edition
- Root tag is always a TAG_Compound (sometimes TAG_List)
- The root tag's name is typically an empty string
- Files are usually **GZip-compressed** (some are uncompressed or zlib-compressed)

### Bedrock Edition
- Root tag is a TAG_Compound (sometimes TAG_List)
- All numbers are **little-endian**
- `level.dat` is **uncompressed** with an 8-byte header:
  - 4 bytes: version (little-endian int)
  - 4 bytes: file length minus header (little-endian int)

## Common File Types

| File | Compression | Notes |
|------|-------------|-------|
| `level.dat` | GZip | Root compound, world settings |
| `<player>.dat` | GZip | Player data |
| `idcounts.dat` | GZip | Map ID counter |
| `villages.dat` | GZip | Village data |
| `raids.dat` | GZip | Raid data |
| `map_<#>.dat` | GZip | Map item data |
| `servers.dat` | Uncompressed | Server list |
| `hotbar.nbt` | Uncompressed | Saved hotbars |
| `scoreboard.dat` | GZip | Scoreboard data |
| Chunks (in region files) | Zlib/GZip | World chunk data |

## Inconsistencies to Watch For

1. **Empty lists**: Older versions may represent them as TAG_List of TAG_Byte; newer versions use TAG_List of TAG_End. Both are valid but can break naive parsers.

2. **Heterogeneous lists**: SNBT allows `[1, "abc"]` but binary NBT does not. When saved, non-compound entries are wrapped: `[1, "abc"]` → list of compounds `[{"":1}, {"":"abc"}]`.

3. **Maximum depth**: Compounds and Lists cannot be nested beyond 512 levels. Parsers should track depth.

4. **TAG_String size field is unsigned**: The 2-byte length prefix for strings is unsigned (0-65535), unlike most other size fields which are signed ints.

## Pseudo-Code for Reading NBT

```
function readTag():
    type = readByte()
    if type == 0:  // TAG_End
        return EndTag
    
    name = readString()  // 2B unsigned len + UTF-8
    
    switch type:
        case 1:  return ByteTag(name, readByte())
        case 2:  return ShortTag(name, readShort())
        case 3:  return IntTag(name, readInt())
        case 4:  return LongTag(name, readLong())
        case 5:  return FloatTag(name, readFloat())
        case 6:  return DoubleTag(name, readDouble())
        case 7:  return ByteArrayTag(name, readByteArray())
        case 8:  return StringTag(name, readString())
        case 9:  return ListTag(name, readList())
        case 10: return CompoundTag(name, readCompound())
        case 11: return IntArrayTag(name, readIntArray())
        case 12: return LongArrayTag(name, readLongArray())

function readString():
    length = readUnsignedShort()
    return readUTF8(length)

function readCompound():
    tags = {}
    while true:
        tag = readTag()
        if tag.type == 0:  // TAG_End
            break
        tags[tag.name] = tag
    return tags

function readList():
    contentType = readByte()
    size = readInt()
    items = []
    for i in 0..size:
        items.append(readPayload(contentType))  // No ID or name
    return items
```
