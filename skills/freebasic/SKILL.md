---
name: freebasic
description: FreeBASIC programming language skill for AI code assistants
---

# FreeBASIC Skill

FreeBASIC is a free/open source, BASIC compiler for Linux, Windows, and DOS.

## Detection

This skill activates when working with FreeBASIC code or projects. Watch for:

**File extensions:** `.bas`, `.bi`

**Comments:**
```freebasic
' FreeBASIC comment
```

**Language markers:**
- `Dim`, `Var`, `Function`, `Sub`, `Print`, `Input`, `If`, `For`, `While`
- `#if`, `#define`, `#include` (preprocessor)
- `End Function`, `End Sub`, `End Type`
- Compiler options: `-lang fb`, `-lang qb`, `-lang fblite`
- Meta-statements: `$Dynamic`, `$Static`, `$Include`

## Quick Reference

### Keywords

| Keyword | Description | Doc |
|---------|-------------|-----|
| Dim, Var | Declare variables | [types.md](types.md) |
| Function, Sub | Define procedures | [procedures.md](procedures.md) |
| If, Then, Else | Conditional execution | [control-flow.md](control-flow.md) |
| For, While, Do | Loops | [control-flow.md](control-flow.md) |
| Print, Input | Console I/O | [basics.md](basics.md) |
| Open, Close, Get, Put | File I/O | [file-io.md](file-io.md) |
| String, Len, Mid | String operations | [strings.md](strings.md) |
| Screen, Circle, Line | Graphics | [graphics.md](graphics.md) |

### API Search

Use the search script to find keywords:

```bash
python scripts/search-api.py "print to screen" --top 5
python scripts/search-api.py --name "Print" -v
python scripts/search-api.py --json "array dimension"
python scripts/search-api.py --list-categories
```

## Topic Routing

### Language Fundamentals

| Task | Doc |
|------|-----|
| Hello World, first program | [basics.md](basics.md) |
| Variables and data types | [types.md](types.md) |
| Operators and expressions | [operators.md](operators.md) |
| Control flow (if, for, while) | [control-flow.md](control-flow.md) |
| Functions and subs | [procedures.md](procedures.md) |
| Arrays and dynamic memory | [arrays.md](arrays.md) |
| Strings and string functions | [strings.md](strings.md) |

### Data Types

| Task | Doc |
|------|-----|
| Integer, Double, Boolean | [types.md](types.md) |
| User-defined types (UDT) | [user-defined-types.md](user-defined-types.md) |
| Pointers and memory | [pointers.md](pointers.md) |
| Type casting and conversion | [types.md](types.md) |

### Standard Library

| Task | Doc |
|------|-----|
| File I/O (Open, Print#, Get, Put) | [file-io.md](file-io.md) |
| Console I/O (Print, Input, Color) | [basics.md](basics.md) |
| Date and time functions | [date-time.md](date-time.md) |
| Math functions (Abs, Sin, Cos) | [math.md](math.md) |
| Memory allocation | [pointers.md](pointers.md) |

### Graphics & UI

| Task | Doc |
|------|-----|
| Screen modes and drawing | [graphics.md](graphics.md) |
| User input (mouse, keyboard) | [graphics.md](graphics.md) |
| Images and sprites | [graphics.md](graphics.md) |

### Advanced Topics

| Task | Doc |
|------|-----|
| Preprocessor directives | [preprocessor.md](preprocessor.md) |
| Threading and synchronization | [threading.md](threading.md) |
| Error handling (On Error) | [error-handling.md](error-handling.md) |
| Compiler options and dialects | [compiler.md](compiler.md) |
| QB migration guide | [compiler.md](compiler.md) |

## Syntax Examples

### Hello World
```freebasic
Print "Hello, World!"
```

### Variables
```freebasic
Dim As Integer x = 10
Dim As Double pi = 3.14159
Dim As String name = "FreeBASIC"
```

### Arrays
```freebasic
Dim array(0 To 9) As Integer
Dim matrix(1 To 3, 1 To 3) As Double
ReDim Preserve array(0 To 20)
```

### Control Flow
```freebasic
If x > 0 Then
    Print "positive"
ElseIf x < 0 Then
    Print "negative"
Else
    Print "zero"
End If

For i As Integer = 1 To 10
    Print i
Next

Do While condition
    ' ...
Loop
```

### Functions
```freebasic
Function Add(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Sub SayHello(name As String)
    Print "Hello, " + name + "!"
End Sub
```

## Dependencies

- FreeBASIC compiler (fbc)
- Python 3.10+ for search scripts

## See Also

- [FreeBASIC Manual](https://www.freebasic.net/wiki/DocToc)
- [Official Website](https://freebasic.net/)
- [Community Forum](https://freebasic.net/forum/)