See also: [basics.md](basics.md) for fundamentals, [snbt.md](snbt.md) for SNBT syntax, [binary-format.md](binary-format.md) for binary format

# NBT Examples

Real-world NBT patterns from Minecraft commands and save files.

## Entity Data

### Basic Entity Properties

```snbt
# Common entity tags
{Health:20f, AbsorptionAmount:0f, Fire:-1s, Air:300s, OnGround:1b, FallDistance:0f, Invulnerable:0b, NoAI:0b, Silent:0b, NoGravity:0b, Glowing:0b, HasVisualFire:0b}
```

### Position and Rotation

```snbt
# Position (double list)
{Pos:[1.5d, 64.0d, 3.5d]}
# Rotation (float list — yaw, pitch)
{Rotation:[0.0f, 0.0f]}
# Motion
{Motion:[0.0d, -0.078d, 0.0d]}
```

### Custom Name and Display

```snbt
# Custom name (JSON text as string)
{CustomName:'{"text":"Boss Mob","color":"red","bold":true}'}
# Visible custom name
{CustomNameVisible:1b}
```

### Tags (String Tags for Grouping)

```snbt
{Tags:["boss", "fire_immune", "quest_mob"]}
```

## Mob Data

### Zombie with Equipment

```snbt
/summon zombie ~ ~ ~ {
    Health:40f,
    HandItems:[
        {id:"minecraft:iron_sword", Count:1b, tag:{Damage:5, Enchantments:[{id:"minecraft:sharpness", lvl:3s}]}},
        {}
    ],
    ArmorItems:[
        {id:"minecraft:leather_boots", Count:1b},
        {id:"minecraft:leather_leggings", Count:1b},
        {id:"minecraft:leather_chestplate", Count:1b},
        {id:"minecraft:leather_helmet", Count:1b}
    ],
    HandDropChances:[0.1f, 0.0f],
    ArmorDropChances:[0.1f, 0.1f, 0.1f, 0.1f]
}
```

### Villager with Trades

```snbt
/summon villager ~ ~ ~ {
    VillagerData:{profession:"minecraft:librarian", level:5, type:"minecraft:plains"},
    Offers:{Recipes:[
        {buy:{id:"minecraft:emerald", Count:1b}, sell:{id:"minecraft:enchanted_book", Count:1b}, maxUses:3, rewardExp:1b},
        {buy:{id:"minecraft:book", Count:1b}, buyB:{id:"minecraft:emerald", Count:5b}, sell:{id:"minecraft:enchanted_book", Count:1b}, maxUses:12, rewardExp:1b}
    ]}
}
```

## Item Data

### Item Structure

```snbt
{
    id:"minecraft:diamond_sword",
    Count:1b,
    tag:{
        Damage:0,
        display:{Name:'{"text":"Epic Blade","italic":false}'},
        Enchantments:[
            {id:"minecraft:sharpness", lvl:5s},
            {id:"minecraft:unbreaking", lvl:3s}
        ]
    }
}
```

### Item Components (1.20.5+)

```snbt
# Modern component-based items
/give @p diamond_sword[minecraft:custom_name='"Epic Blade"', minecraft:damage=10, minecraft:enchantments={levels:{"minecraft:sharpness":5}}]

# In NBT form (for custom_data context):
{custom_data:{rarity:"legendary", origin:"dragon_loot"}}
```

## Block Entity Data

### Chest

```snbt
{
    Items:[
        {Slot:0b, id:"minecraft:diamond", Count:64b},
        {Slot:1b, id:"minecraft:iron_ingot", Count:32b},
        {Slot:13b, id:"minecraft:emerald", Count:16b}
    ],
    Lock:"",
    LootTable:"",
    LootTableSeed:0L,
    CustomName:'{"text":"Treasure Chest"}'
}
```

### Command Block

```snbt
{
    Command:"say Hello World",
    SuccessCount:0,
    powered:0b,
    auto:0b,
    conditionMet:0b,
    UpdateLastExecution:1b,
    LastOutput:"",
    TrackOutput:1b
}
```

### Sign

```snbt
{
    Text1:'{"text":"Line 1","color":"red"}',
    Text2:'{"text":"Line 2","color":"gold"}',
    Text3:'{"text":"Line 3"}',
    Text4:'{"text":"Line 4"}',
    Color:"black",
    GlowingText:0b
}
```

## Storage and Data Commands

### Command Storage

```snbt
# Store data in command storage
/data merge storage minecraft:my_pack {counter:0, players:["Steve","Alex"]}

# Read from storage
/data get storage minecraft:my_pack counter

# Modify a value
/data modify storage minecraft:my_pack counter set value 42
```

### Execute with NBT Checks

```snbt
# Check if entity has tag
/execute if entity @e[nbt={Tags:["boss"]}, limit=1] run say Boss detected

# Check nested NBT
/execute if entity @a[nbt={Inventory:[{id:"minecraft:diamond"}]}, limit=1] run say Someone has diamonds

# Check recipe progress
/execute if data entity @s RecipeBook{isFurnaceFilteringCraftable:1b} run say Furnace filter enabled
```

## JSON ↔ NBT Conversion Contexts

### Loot Table Conditions (JSON → NBT)

```json
{
  "condition": "minecraft:match_tool",
  "predicate": {
    "nbt": "{Enchantments:[{id:\"minecraft:silk_touch\",lvl:1s}]}"
  }
}
```

### Biome Particle Config (NBT → JSON)

```snbt
# In biome definition: ambient particle settings
{
    particle:{
        options:{
            type:"minecraft:end_rod",
            value:{probability:0.001f}
        }
    }
}
```

## Common Pitfalls

### Type Confusion

```
# WRONG: int vs byte
{Health:20}      # int 20, but Health expects a float → converted to 0f
{Health:20f}     # Correct: float 20

# WRONG: namespace missing
{Item:{id:"stone"}}           # won't match anything
{Item:{id:"minecraft:stone"}} # Correct

# WRONG: list vs array
{Tags:[]}         # empty list vs populated list — wrong if checking for empty
{Tags:["a","b"]}  # list of strings — correct

# WRONG: array prefix confusion
[1,2,3]           # List of ints
[I;1,2,3]         # Int Array — different type!
```

### Type Suffix Notes

```
# Int (no suffix) and Double (no decimal = int)
{Hp: 20}          # Hp is TAG_Int(20)
{Speed: 0.5}      # Speed is TAG_Double(0.5)

# But in entity data, Health EXPECTS a float — providing int may convert to 0
{Health: 20}      # TAG_Int → converted → Health = 0!
{Health: 20f}     # TAG_Float → Correct
```

### Testing Gotchas

```
# Testing: {Tags:[]} only matches entities with truly empty Tags list
# Most entities have no Tags tag at all, so {} matches but {Tags:[]} does not

# Position: list matching ignores order!
# Entity has {Pos:[1d,2d,3d]}
# {Pos:[2d]} matches! (element exists somewhere in list)

# But arrays check order:
# {UUID:[I;1,2,3,4]} must match exactly in position and type
```
