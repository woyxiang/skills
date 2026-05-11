See also: [basics.md](basics.md) for fundamentals, [binary-format.md](binary-format.md) for binary format, [examples.md](examples.md) for real-world SNBT

# SNBT (Stringified NBT)

SNBT is the text representation of NBT used in Minecraft Java Edition commands and `.snbt` files. It is JSON5-like but with type suffixes on numbers and array prefix notation.

## Data Types in SNBT

### Byte
- **Suffix**: `b` or `B`
- **Range**: -128 to 127
- **Format**: `<number>b`
- **Examples**: `34B`, `-20b`, `0x1b`

### Boolean
- NBT has no boolean type. `true` and `false` are syntactic sugar for `1b` and `0b`.
- **Format**: `true`, `false`
- **Note**: Only in SNBT; stored as byte in binary NBT.

### Short
- **Suffix**: `s` or `S`
- **Range**: -32,768 to 32,767
- **Format**: `<number>s`
- **Examples**: `31415s`, `-27183s`

### Int
- **Suffix**: none, or `i`/`I`
- **Range**: -2,147,483,648 to 2,147,483,647
- **Format**: `<integer>` (default for whole numbers without decimal)
- **Examples**: `31415926`, `42i`

### Long
- **Suffix**: `l` or `L`
- **Range**: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- **Format**: `<number>l`
- **Examples**: `31415926l`, `-1L`

### Float
- **Suffix**: `f` or `F`
- **Range**: ~±3.4E38 (IEEE 754 single-precision)
- **Format**: `<number>f`
- **Examples**: `3.1415926f`, `1e10f`

### Double
- **Suffix**: none, or `d`/`D`
- **Range**: ~±1.79E308 (IEEE 754 double-precision)
- **Format**: `<decimal>` (default for numbers with decimal point or E notation)
- **Examples**: `3.1415926`, `3.0d`

### String
- **Quoted format**: `"text"` or `'text'`
- **Unquoted format**: Allowed if string contains only `[a-zA-Z0-9_\-.+]+` and does NOT start with a digit, `-`, `.`, or `+`
- **Escaping**: `\"` or `\'` for nested quotes; `\\` for backslash; plus escape sequences (see below)
- **Examples**:
  - `"Hello \"World!\""`
  - `'Hello "World!"'`
  - `simple_string` (unquoted, no special chars)

### List
- **Format**: `[value, value, ...]` — unnamed tags of the same type, comma-separated
- **Homogeneous** in binary NBT; heterogeneous allowed in SNBT (converted on save)
- **Examples**:
  - `[3.2, 64.5, 129.5]` — list of doubles
  - `["a", "b", "c"]` — list of strings
  - `[1, "abc"]` — heterogeneous (SNBT only; saved as `[{"":1},{"":"abc"}]`)

### Compound
- **Format**: `{key: value, "key": value, ...}` — named tags, comma-separated, unordered
- **Keys**: Unquoted if `[a-zA-Z0-9_\-.+]+` and not starting with digit/`-`/`.`/`+`; otherwise double-quoted or single-quoted
- **Trailing commas**: Allowed
- **Examples**:
  - `{X:3, Y:64, Z:129}`
  - `{foo: 1, bar: "abc", baz: {}}`

### Byte Array
- **Format**: `[B;<byte>, <byte>, ...]`
- **Distinct from** List of bytes: `[B;1b,2b,3b]` ≠ `[1b,2b,3b]`
- **Example**: `[B;1b,2b,true,false]` (true/false in arrays work as 1b/0b)

### Int Array
- **Format**: `[I;<int>, <int>, ...]` — byte/short values promoted to int
- **Distinct from** List of ints: `[I;1,2,3]` ≠ `[1,2,3]`
- **Example**: `[I;1,2,3]`, `[I;1b,2s,3i]`

### Long Array
- **Format**: `[L;<long>, <long>, ...]` — byte/short/int values promoted to long
- **Distinct from** List of longs: `[L;1l,2l,3l]` ≠ `[1l,2l,3l]`
- **Example**: `[L;1l,2l,3l]`, `[L;1b,2s,3i,4l]`

## Number Format Variants

### Suffix Order

When two suffixes are present, the first is signedness (`s`/`u`), the second is data type (`b`, `s`, `i`, `l`, `f`, `d`).

When one suffix is present, it represents the data type. Default signedness is signed.

| Value | Meaning |
|-------|---------|
| `15s` | Signed short `15` |
| `15sS` | Signed short `15` (explicit) |
| `15Us` | Unsigned short `15` |
| `-16b` | Signed byte `-16` |
| `-16sb` | Signed byte `-16` (explicit) |
| `240uB` | Unsigned byte 240 → byte `-16` |
| `82u` | ERROR — signedness must be followed by data type |
| `30bu` | ERROR — data type must follow signedness |

### Number Literal Features

```
# Hexadecimal
0xbad, 0xCAFE, 0xFFb

# Binary
0b101, 0b1001_0110b

# E notation (floats)
1.2e3, 87E48, 0.1e-1

# Underscore separators
0b10_01, 0xAB_CD, 1_2.3_4__5f, 1_2e3_4

# Omitted whole/fraction parts
.1, 1., .5f

# Unsigned hex byte (must have signedness suffix since b is a hex digit)
0x11ub, 0x11sb
```

### Default Type Inference (no suffix)

| Number form | Inferred type |
|-------------|---------------|
| Integer (no decimal, no E) | Int |
| Decimal or E notation | Double |

### SNBT → Binary Type Inference (command parsing)

When parsing SNBT without explicit suffixes:
1. If there's a decimal point → Double
2. If there's no decimal point → Int
3. Suffix letter overrides: `B/S/L/F/D` (case-insensitive)

## Escape Sequences

Valid in quoted strings (`"..."` or `'...'`):

| Escape | Hex (ASCII) | Character |
|--------|-------------|-----------|
| `\b` | 08 | Backspace |
| `\f` | 0C | Form feed |
| `\n` | 0A | Newline (Line Feed) |
| `\r` | 0D | Carriage Return |
| `\s` | 20 | Space |
| `\t` | 09 | Horizontal Tab |
| `\\` | 5C | Backslash |
| `\'` | 27 | Single quote |
| `\"` | 22 | Double quote |
| `\xhh` | hh | Unicode code point below 0x100 (e.g., `\x42`) |
| `\uhhhh` | non-ASCII | Unicode code point below 0x10000 (e.g., `☄`) |
| `\Uhhhhhhhh` | non-ASCII | Unicode code point below 0x100000000 (e.g., `\U00051020`) |
| `\N{name}` | non-ASCII | Named Unicode character (e.g., `\N{Snowman}`) |

## Operations

SNBT supports two built-in operations:

### `bool(arg)`
Converts argument to boolean:
- Boolean argument → returns directly
- Number argument → `false` if 0, `true` otherwise
- String argument → error

```
bool(true)  → true
bool(5)     → true
bool(0)     → false
bool("foo") → error
```

### `uuid(str)`
Converts UUID string to int array:
```
uuid("f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
→ [I; -132296786, 2112623056, -1486552928, -920753162]
```

## SNBT → Programmatic Conversion (Command Parsing)

When the game parses SNBT into a programmatic NBT object:

| SNBT | NBT Object Rule |
|------|----------------|
| Number with suffix | Resolved to corresponding type |
| Number without suffix | Double if decimal point, Int otherwise |
| `true` / `false` | `1b` / `0b` |
| `[B;...]` | Byte Array |
| `[I;...]` | Int Array |
| `[L;...]` | Long Array |
| `[...]` without prefix | List |
| `["...": ...]` or `{key:...}` | Compound |

## Programmatic → SNBT Conversion (Output)

When the game outputs NBT as SNBT (e.g., `/data get`):

- Numbers always followed by type suffix (lowercase for `b/s/f/d`, uppercase for `L`)
- Int has no suffix (default)
- Strings always quoted; double-quotes preferred unless string contains `"`, then single-quotes; if both present, uses whichever appears last first
