For command line usage, see [basics.md](basics.md).
For dialects, see [compiler.md](compiler.md).

# Compiler Options and Dialects

## Command Line

```bash
fbc myprogram.bas              # compile
fbc -s console prog.bas        # console subsystem
fbc -s gui prog.bas            # GUI subsystem
fbc -exx prog.bas              # extended error checking
```

## Compiler Options

| Option | Description |
|--------|-------------|
| -lang fb/qb/fblite | Set dialect |
| -e | Enable runtime error checking |
| -ex | Error checking with Resume support (needed for On Error handlers) |
| -exx | Extended error checking (array bounds, null ptr, division by zero) |
| -module name | Create module |
| -export | Export symbols |
| -profile | Enable profiling |
| -target triplet | Cross-compile |

## Dialects

### -lang fb (default)
Modern FreeBASIC with all features.

```freebasic
#lang "fb"
Dim As Integer x = 10
```

### -lang qb
QBASIC compatibility mode.

```freebasic
#lang "qb"
x = 10  ' without Dim
```

### -lang fblite
Moderated compatibility.

```freebasic
#lang "fblite"
Dim As Integer x
```

## Meta-statements

```freebasic
'$lang: "fb"
'$dynamic
'$static
'$include "file.bi"
```

## QB to FB Migration

```freebasic
' QB style (DEFINT and suffixes need -lang fblite/qb)
#lang "fblite"

DEFINT A-Z
FOR I = 1 TO 10
    PRINT I
NEXT I

' FB style
For j As Integer = 1 To 10
    Print j
Next
```

## Preprocessor

```bash
fbc -d DEBUG myprogram.bas     # define DEBUG symbol
```

## Optimization

| Option | Description |
|--------|-------------|
| -O 0 | No optimization |
| -O 1 | Basic |
| -O 2 | Full |
| -O 3 | Extra |

## Error Messages

```bash
fbc -exx prog.bas    # extra error info
```

## See Also

- [basics.md](basics.md) - Compiler invocation
- [preprocessor.md](preprocessor.md) - Preprocessor directives
- [user-defined-types.md](user-defined-types.md) - QB type keywords