---
name: minecraft-nbt
description: 'To understand Minecraft NBT (Named Binary Tag) format. Use when: (1) user references NBT, SNBT, or Named Binary Tag, (2) user works with Minecraft commands using data tags (curly-brace syntax), (3) user mentions .dat, .nbt, level.dat, or Minecraft save files, (4) user needs to parse, generate, or validate NBT/SNBT data, (5) user asks about NBT tag types like TAG_Byte, TAG_Compound, etc., (6) code or context contains NBT-format binary data or SNBT strings'
---

# Minecraft NBT Format

Named Binary Tag (NBT) is the tree-structured data format used by Minecraft to store game data in save files and to pass structured data in commands.

## Detection

**File patterns:** `*.dat`, `*.nbt`, `level.dat`, `*.snbt`
**Keywords:** `NBT`, `SNBT`, `Named Binary Tag`, `TAG_Byte`, `TAG_Compound`, `TAG_List`, `TAG_End`
**SNBT patterns:** Curly-brace data in Minecraft commands (e.g., `{Health:20f,Inventory:[...]}`)
**Binary patterns:** GZip-compressed files containing tag ID bytes (0x00-0x0C)
**Contexts:** Minecraft commands (`/data`, `/execute`, `/summon`, `/give`), save file parsing

## Routing

| When you need to... | Read |
|---|---|
| Understand what NBT is and how it's used | [basics.md](basics.md) |
| Work with SNBT (the string/text format used in commands) | [snbt.md](snbt.md) |
| Parse or write binary NBT data | [binary-format.md](binary-format.md) |
| See real-world NBT examples from Minecraft commands | [examples.md](examples.md) |

## Two Faces of NBT

NBT exists in two forms:

1. **Binary NBT** — The on-disk format used in save files (`.dat`, `.nbt`, chunk data). A tree of typed tags with numeric IDs, usually GZip-compressed.
2. **SNBT (Stringified NBT)** — The text format used in Minecraft commands and data generators (`.snbt` files). Human-readable JSON-like syntax.

## Quick Reference

### Tag Types (Binary IDs)

| ID | Tag | Payload |
|----|-----|---------|
| 0 | TAG_End | None (marks end of compound) |
| 1 | TAG_Byte | 1 byte, signed |
| 2 | TAG_Short | 2 bytes, signed, big-endian |
| 3 | TAG_Int | 4 bytes, signed, big-endian |
| 4 | TAG_Long | 8 bytes, signed, big-endian |
| 5 | TAG_Float | 4 bytes, IEEE 754 binary32 |
| 6 | TAG_Double | 8 bytes, IEEE 754 binary64 |
| 7 | TAG_Byte_Array | Int size + bytes |
| 8 | TAG_String | Unsigned short size + UTF-8 bytes |
| 9 | TAG_List | Byte tag ID + int size + payloads |
| 10 | TAG_Compound | Fully formed tags until TAG_End |
| 11 | TAG_Int_Array | Int size + int payloads |
| 12 | TAG_Long_Array | Int size + long payloads |

### SNBT Type Suffixes

| Type | Suffix | Example |
|------|--------|---------|
| Byte | `b`/`B` | `34B`, `-20b` |
| Short | `s`/`S` | `31415s` |
| Int | (none) or `i`/`I` | `31415926` |
| Long | `l`/`L` | `31415926l` |
| Float | `f`/`F` | `3.14f` |
| Double | (none) or `d`/`D` | `3.1415926` |

### Key SNBT Rules

- **Compound keys** can be unquoted if they match `[a-zA-Z0-9_\-.+]+` and don't start with a digit/`-`/`.`/`+`
- **String values** can be unquoted with same rules; otherwise use `"..."` or `'...'`
- **Arrays** vs **Lists**: `[B;1b,2b,3b]` is a byte array; `[1b,2b,3b]` is a list — they are different types
- **Heterogeneous lists**: SNBT allows `[1, "abc"]`; when saved to binary NBT, non-compound entries become compounds with empty-key `{"":value}`
- **Numbers**: Support hex (`0x`), binary (`0b`), E notation, underscore separators, signedness suffixes (`u`/`s`)
- **Boolean**: NBT has no boolean — `true`/`false` in SNBT become `1b`/`0b`

### Key Binary Rules

- **Java Edition**: All multi-byte numbers are **big-endian**
- **Bedrock Edition**: All multi-byte numbers are **little-endian**
- **TAG_End** has no name (just a single `0x00` byte)
- **Root tag** is always a compound (Java) or compound/list (Bedrock), usually with empty string name
- **Nesting limit**: 512 levels deep for List and Compound
- **Files**: Usually GZip-compressed; some are uncompressed or zlib-compressed

### Partial Matching (Testing)

When testing NBT with commands like `/execute if data` or target selector `nbt=`:
- **Compounds**: Extra tags in target still match (subset match). `{}` matches anything.
- **Lists**: Order and count ignored — as long as every requested element is present, it matches. Empty list only matches empty list.
- **Arrays** (byte/int/long): Order and count ARE checked.
- **Types must match exactly**: `1` (int) ≠ `1d` (double)
- **Namespaces required**: `"stone"` ≠ `"minecraft:stone"`

## Java vs Bedrock

| Feature | Java | Bedrock |
|---------|------|---------|
| Endianness | Big-endian | Little-endian |
| level.dat | GZip-compressed | Uncompressed + 8-byte header |
| Heterogeneous lists | Supported in SNBT | N/A |

## Dependencies

No external tools required. For working with NBT files, common tools include:
- **NBTExplorer** / **NBT Studio** — GUI NBT file viewer/editor
- **webNBT** — Online NBT viewer
- Vanilla **data generator** — Converts `.snbt` ↔ `.nbt`

## Validation Patterns

When validating SNBT:
1. Check that all tags have a valid type suffix
2. Verify compound keys are properly quoted if they contain special characters
3. Ensure arrays use the correct prefix (`B;`, `I;`, `L;`)
4. Confirm numbers are within their type's range
5. Check for balanced brackets and braces
6. Verify escape sequences in strings are valid
7. Ensure namespaces are present in resource location strings when testing matches
