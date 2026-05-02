For language basics, see [types.md](types.md) and [operators.md](operators.md).
For control flow, see [control-flow.md](control-flow.md).

# FreeBASIC Basics

FreeBASIC is a modern BASIC compiler supporting multiple dialects (-lang fb, -lang qb, -lang fblite).

## Hello World

```freebasic
Print "Hello, World!"
```

Compile with: `fbc myprogram.bas`

## Program Structure

```freebasic
' Comments start with apostrophe
' Or use REM for comments

' Variable declarations
Dim As Integer x = 10

' Main code
Print "The value is "; x

' End statement (optional)
End 0
```

## Comments

```freebasic
' Single line comment
Rem Another comment style

/' Multi-line
   comment '/

Dim x As Integer ' Inline comment
```

## Console I/O

### Print
```freebasic
Print "Hello"  ' prints with newline
Print "Hello"; "World"  ' semicolon = no space
Print "Value: "; x  ' prints variable

' Comma = column separator (14 char boundary)
Print "Name: "; name, "Age: "; age
```

### Input
```freebasic
Dim name As String
Print "Enter your name: ";
Input name

' With prompt
Input "Your age: ", age

' Line input (get entire line)
Dim line As String
Line Input line
```

### Color and Cursor
```freebasic
Color 12, 0  ' foreground, background
Cls  ' clear screen
Locate row, col  ' position cursor
Print "text"
```

## Compiler

### Command Line
```bash
fbc myprogram.bas        ' compile
fbc -s console myprogram.bas  ' console mode
fbc -lang fb myprogram.bas     ' explicit dialect
```

### Dialects
- `-lang fb` (default): Modern FreeBASIC
- `-lang qb`: QBASIC compatibility
- `-lang fblite`: Moderated compatibility

## See Also

- [types.md](types.md) - Data types and variables
- [control-flow.md](control-flow.md) - If, For, While
- [procedures.md](procedures.md) - Function and Sub
- [operators.md](operators.md) - Operators and expressions