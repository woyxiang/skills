---
name: freebasic
description: 'FreeBASIC (fbc) language reference and coding guide. Use when: (1) Writing, debugging or reviewing FreeBASIC code (.bas, .bi), (2) User mentions FreeBASIC, fbc, -lang fb/qb/fblite, or QBASIC/QB64 migration, (3) Converting VB/QB code to FreeBASIC, (4) Answering questions about FreeBASIC syntax, stdlib, graphics, threading or compiler options'
---

# FreeBASIC Skill

FreeBASIC is a free/open source BASIC compiler for Linux, Windows, and DOS. This skill targets **fbc 1.10.1**; the embedded API index (`data/api.json`) is extracted from the 1.10.1 manual.

## Detection

**File extensions:** `.bas`, `.bi`

**Language markers:**
- `Dim`, `Var`, `Function`, `Sub`, `Print`, `Input`, `If`, `For`, `While`
- `#if`, `#define`, `#include`, `#lang "fb"` (preprocessor)
- `End Function`, `End Sub`, `End Type`
- Compiler options: `-lang fb`, `-lang qb`, `-lang fblite`
- Meta-statements: `'$Dynamic`, `'$Static`, `'$Include`

## Compile and Verify

Code is not done until it compiles. The loop:

```bash
fbc -w all prog.bas -x prog    # compile (warnings on), produce executable
./prog                          # run it, compare output with what you claimed
```

To settle a semantics question, compile a throwaway program instead of guessing:

```bash
printf 'Print CInt(2.5)\n' > /tmp/t.bas && fbc /tmp/t.bas -x /tmp/t && /tmp/t
```

To check every code example in this skill's docs: `python scripts/validate-examples.py`. When verifying output for the user, run the program and diff its actual output against the requirement; report what you ran.

## Common Errors

| Error | Fix |
|-------|-----|
| error 42: Variable not declared | Missing `Dim`, or the function lives in a header (`Now` needs `vbcompat.bi`) - see [debug.md](debug.md) |
| error 4: Duplicated definition | Identifier reused case-insensitively, or it is a reserved word (`name`, `line`, `width`...) |
| error 14: Expected identifier | Reserved word used as a name (`Dim x As Date` - there is no Date type) |
| error 146/147: Only valid in -lang deprecated or fblite or qb | `Resume`, `DEFINT`, suffixes, `'$Dynamic` need the QB dialects |
| error 17: Syntax error in `#lang fb` | Quotes required: `#lang "fb"` |
| error 61: Illegal inside functions | Sub/Function nested inside another, or module-level statement in a procedure |

More traps (VB functions that do not exist, banker's rounding, `Err` resetting, precedence surprises): [debug.md](debug.md).

## Topic Routing

### Language Fundamentals

| Task | Doc |
|------|-----|
| Hello World, first program, console I/O | [basics.md](basics.md) |
| Variables and data types | [types.md](types.md) |
| Operators, expressions, precedence | [operators.md](operators.md) |
| Control flow (if, for, while, select) | [control-flow.md](control-flow.md) |
| Functions and subs | [procedures.md](procedures.md) |
| Arrays | [arrays.md](arrays.md) |
| Strings and string functions | [strings.md](strings.md) |

### Data Types

| Task | Doc |
|------|-----|
| Integer, Double, Boolean | [types.md](types.md) |
| User-defined types (UDT), constructors, unions | [user-defined-types.md](user-defined-types.md) |
| Pointers, memory, function pointers | [pointers.md](pointers.md) |
| Type casting and conversion | [types.md](types.md) |

### Standard Library

| Task | Doc |
|------|-----|
| File I/O (Open, Print#, Get, Put, Seek) | [file-io.md](file-io.md) |
| Console I/O (Print, Input, Color, Locate) | [basics.md](basics.md) |
| Date and time (needs vbcompat.bi) | [date-time.md](date-time.md) |
| Math functions (Abs, Sin, Atn, Rnd) | [math.md](math.md) |
| Memory allocation | [pointers.md](pointers.md) |

### Graphics & UI

| Task | Doc |
|------|-----|
| Screen modes and drawing | [graphics.md](graphics.md) |
| User input (mouse, keyboard, MultiKey) | [graphics.md](graphics.md) |
| Images and sprites | [graphics.md](graphics.md) |

### Advanced Topics

| Task | Doc |
|------|-----|
| Preprocessor directives, macros | [preprocessor.md](preprocessor.md) |
| Threading and synchronization | [threading.md](threading.md) |
| Error handling (On Error, Err, -ex) | [error-handling.md](error-handling.md) |
| Compiler options and dialects | [compiler.md](compiler.md) |
| QB/VB migration, dialect differences | [compiler.md](compiler.md), [debug.md](debug.md) |
| Bugs, gotchas, "why does this compile wrong" | [debug.md](debug.md) |

## API Search

The skill embeds the full 1.10.1 keyword index (626 entries with syntax, parameters, examples):

```bash
python scripts/search-api.py "print to screen"       # full-text search
python scripts/search-api.py --name Print -v         # exact keyword lookup
python scripts/search-api.py --name "?"              # aliases work
python scripts/search-api.py --list-categories       # browse categories
python scripts/search-api.py "array" --json          # machine-readable
```

## Starter Programs

Copy the closest starter, adjust, compile - faster than starting from blank:

| Example | Start here when you want... |
|---------|------------------------------|
| [console-app.bas](examples/console-app.bas) | A console program: input, loops, functions |
| [file-report.bas](examples/file-report.bas) | File I/O and text processing |

## Syntax Examples

### Hello World
```freebasic
Print "Hello, World!"
```

### Variables
```freebasic
Dim As Integer x = 10
Dim As Double pi = 3.14159
Dim As String s = "FreeBASIC"
```

### Arrays
```freebasic
Dim array(0 To 9) As Integer
Dim matrix(1 To 3, 1 To 3) As Double
ReDim Preserve array(0 To 20)
```

### Functions
```freebasic
Function Add(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Sub SayHello(ByVal msg As String)
    Print "Hello, " + msg + "!"
End Sub
```

## Dependencies

- FreeBASIC compiler (fbc) 1.10.x
- Python 3.10+ for search/validate scripts

## See Also

- [FreeBASIC Manual](https://www.freebasic.net/wiki/DocToc)
- [Official Website](https://freebasic.net/)
- [Community Forum](https://freebasic.net/forum/)
