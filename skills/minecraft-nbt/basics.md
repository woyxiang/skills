See also: [snbt.md](snbt.md) for SNBT syntax details, [binary-format.md](binary-format.md) for binary format

# NBT Fundamentals

## What is NBT?

Named Binary Tag (NBT) is a tree data structure used by Minecraft to store arbitrary data. Every piece of data in an NBT tree is a "tag" — a typed value with a name. Tags form a hierarchy: compounds contain named tags, lists contain unnamed tags of a single type, and leaf tags hold primitive values.

NBT is used in:
- **Save files**: `level.dat`, player data, chunk data, scoreboard data, etc.
- **Commands**: `/data`, `/execute`, `/summon`, `/give`, target selectors
- **Data generation**: Structure files, configured features, loot tables (via JSON→NBT)

## The Two Representations

### Binary NBT (on-disk format)

The on-disk format is a binary stream of typed tags. Each tag starts with a 1-byte type ID, followed by a name (2-byte length prefix + UTF-8), then the type-specific payload. The root is almost always a compound tag. Files are typically GZip-compressed in Java Edition; uncompressed or zlib-compressed in some cases.

```
[type:1B][name_len:2B][name:N*UTF-8][payload...]
```

### SNBT (string/text format)

Stringified NBT is the human-readable text form used in commands and `.snbt` files. It resembles JSON5: unquoted keys, type suffixes on numbers, array prefixes (`B;`, `I;`, `L;`), and single/double quoted strings.

```snbt
{Health:20f, Tags:["friendly","quest_giver"], Inventory:[...]}
```

## Tag Categories

### Numeric Tags (6 types)

| Tag | Bits | Range |
|-----|------|-------|
| Byte | 8-bit signed | -128 to 127 |
| Short | 16-bit signed | -32,768 to 32,767 |
| Int | 32-bit signed | ~-2.1B to ~2.1B |
| Long | 64-bit signed | ~-9.2e18 to ~9.2e18 |
| Float | 32-bit IEEE 754 | ~±3.4e38 |
| Double | 64-bit IEEE 754 | ~±1.8e308 |

### String Tag

UTF-8 text, max 65,535 bytes. Used for text data, resource locations (namespaced IDs), and JSON text components.

### Container Tags

| Tag | Ordered? | Elements named? | Mixed types? |
|-----|----------|-----------------|--------------|
| Compound | No (unordered) | Yes | Yes |
| List | Yes | No | No (same type) |
| Byte Array | Yes | No | N/A (bytes only) |
| Int Array | Yes | No | N/A (ints only) |
| Long Array | Yes | No | N/A (longs only) |

**Key distinction**: `[B;1b,2b,3b]` (Byte Array) is NOT the same as `[1b,2b,3b]` (List of Bytes). They are different tag types with different type IDs.

### Special Tags

- **TAG_End** (ID 0): Marks the end of a compound. Has no name, no payload — just a single `0x00` byte. Also used as the content type for empty lists in newer Minecraft versions.

## NBT in Minecraft Commands

### Data Commands

```
/data get entity @s                           # Get all data
/data get entity @s Health                    # Get specific tag
/data merge entity @s {Health:20f}            # Merge data (partial update)
/data modify entity @s Health set value 20f   # Modify specific tag
/data remove entity @s CustomName             # Remove tag
```

### Target Selectors with NBT

```
@e[nbt={Tags:["boss"]}]               # Entities with "boss" tag
@e[nbt={Brain:{memories:{}}}}]         # Entities with specific nested structure
@a[nbt={Inventory:[{id:"minecraft:diamond"}]}]  # Players with diamond
```

### Spawn/Summon with NBT

```
/summon zombie ~ ~ ~ {Health:40f,HandItems:[{id:"minecraft:iron_sword",Count:1b},{}]}
/give @p diamond_sword[minecraft:damage=10, minecraft:custom_name='"Epic Blade"']
```

## Partial Matching (NBT Testing)

When the game tests one NBT object against another (e.g., `/execute if data`, `nbt=` selector):

1. The SNBT pattern is parsed into an NBT object
2. The target's NBT object is obtained
3. A contains-check is performed (not equality)

**Compound matching**: Every key in the pattern must exist in the target with a matching value. The target may have additional keys. An empty compound `{}` always matches.

**List matching**: Every element in the pattern list must exist somewhere in the target list (order ignored). An empty list `[]` only matches another empty list.

**Array matching**: Elements AND order are checked. Arrays behave like strict equality checks.

**Type matching**: Types must match exactly. `1` (int) does not match `1d` (double). `"stone"` does not match `"minecraft:stone"` — namespaces are required in NBT objects.

## Conversion Rules

When the game converts tags between types (e.g., SNBT → programmatic → entity property):

| Target property needs | Source tag is non-matching | Result |
|-----------------------|---------------------------|--------|
| Boolean | Numeric tag | `true` if non-zero after rounding to byte |
| Boolean | Non-numeric tag | `false` |
| Numeric | Non-numeric tag | `0` |
| String | Non-string tag | Empty string `""` |
| List/Array | Wrong type | Empty list/array |
| Compound | Non-compound | Empty compound |
| Resource Location | String | String parsed as resource location |
| JSON Text | String | String parsed as JSON text |
