---
name: freebasic
description: >
  Guide for programming in FreeBASIC, a free/open-source BASIC compiler syntax-compatible with QuickBASIC.
  Use this skill when the user asks to write, debug, explain, or convert FreeBASIC code, or when working
  with .bas files, the fbc compiler, or any FreeBASIC-specific language features. Also use when migrating
  QuickBASIC code to FreeBASIC, exploring FreeBASIC data types, procedures, control flow, OOP features,
  graphics, threading, or file I/O. The skill references the official FreeBASIC wiki documentation bundled
  in the references/ directory.
---

# FreeBASIC Programming Skill

FreeBASIC is a free, open-source (GPL) compiler syntax-compatible with QuickBASIC, targeting Windows, DOS, and Linux. It extends BASIC with modern features: pointers, OOP, operator overloading, multithreading, inline assembly, and a rich runtime library.

## Quick Reference: How to Use This Skill

1. **Identify the topic** the user is asking about (variables, control flow, procedures, etc.)
2. **Consult the relevant reference file(s)** listed below to get accurate syntax and semantics
3. **Write or explain FreeBASIC code** using idiomatic patterns from the documentation
4. Always compile with `fbc <filename>.bas` unless the user specifies otherwise

## Language Fundamentals

### Dialects
FreeBASIC has three dialects controlled by `-lang`:
- **`fb`** (default): Modern FreeBASIC. Requires explicit variable declarations (`Option Explicit` is implied). Full feature set.
- **`fblite`**: Compatibility mode. Implicit variables allowed, more QB-like.
- **`qb`**: Maximum QuickBASIC compatibility.

Reference: `references/CompilerDialects.html`

### Compilation
Compile with: `fbc [options] <source.bas>`
Key options: `-lang fb|qb|fblite`, `-gen gas|gcc`, `-m <name>`, `-x <output>`, `-s gui|console`

Reference: `references/CompilerCmdLine.html`, `references/CatPgCompOpt.html`

## Variables and Data Types

Declare variables with `Dim`. Use `Var` for type inference from initializers.

### Numeric Types
| Type | Size | Format | Suffix |
|------|------|--------|--------|
| Byte | 8-bit | signed integer | |
| UByte | 8-bit | unsigned integer | |
| Short | 16-bit | signed integer | |
| UShort | 16-bit | unsigned integer | |
| Integer | 32/64-bit | signed integer | % |
| UInteger | 32/64-bit | unsigned integer | u |
| Long | 32-bit | signed integer | &, l |
| ULong | 32-bit | unsigned integer | ul |
| LongInt | 64-bit | signed integer | ll |
| ULongInt | 64-bit | unsigned integer | ull |
| Single | 32-bit | floating point | !, f |
| Double | 64-bit | floating point | #, d |

`Integer`/`UInteger` are pointer-sized (32-bit on x86, 64-bit on x86_64).

Reference: `references/TblVarTypes.html`, `references/CatPgStdDataTypes.html`

### String Types
- `String`: Variable-length, managed string
- `ZString * N`: Fixed-length, null-terminated (C interop)
- `WString * N`: Wide (Unicode) string

Reference: `references/CatPgString.html`, `references/ProPgStringsTypes.html`

### Key Declarations
- `Dim name As Type` — declare variable
- `Dim name As Type = value` — declare with initializer
- `Var name = value` — type-inferred declaration
- `Const name As Type = value` — constant
- `Static name As Type` — persistent variable in procedures
- `Shared name As Type` — module-visible variable
- `ByRef refname As Type = original` — reference alias

Reference: `references/CatPgVariables.html`, `references/KeyPgDim.html`

### User-Defined Types
```freebasic
Type MyType
    field1 As Integer
    field2 As String
    Declare Constructor()
    Declare Sub Method()
End Type
```
Supports: constructors, destructors, member functions, properties, inheritance (`Extends`), abstract classes, interfaces (`Implements`), access control (`Public`, `Private`, `Protected`), operator overloading.

Reference: `references/CatPgUserDefTypes.html`, `references/ProPgUDTs.html`, `references/ProPgTypeObjects.html`

## Control Flow

### Branching
- `If...Then...ElseIf...Else...End If`
- `Select Case...Case...Case Else...End Select`
- `IIf(condition, true_val, false_val)` — inline conditional

### Looping
- `For counter = start To end [Step step]...Next`
- `Do [While|Until condition]...Loop` or `Do...Loop [While|Until condition]`
- `While condition...Wend`

### Loop/Block Control
- `Exit For`, `Exit Do`, `Exit While`, `Exit Select` — break out
- `Continue For`, `Continue Do`, `Continue While` — skip to next iteration

Reference: `references/CatPgControlFlow.html`

## Procedures

### Sub and Function
```freebasic
Sub MySub(ByVal x As Integer, ByRef s As String)
    ' no return value
End Sub

Function MyFunc(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function
```

- `ByVal` (default): pass a copy
- `ByRef`: pass a reference (alias to original)
- `ByRef Function`: function returns by reference
- `Overload`: multiple procedures with same name, different signatures
- `Declare`: forward declaration
- `Function Ptr`: procedure pointers

### Calling Conventions
`StdCall` (default), `Cdecl`, `Pascal`, `FastCall`, `ThisCall`

Reference: `references/CatPgProcedures.html`, `references/ProPgProcedures.html`, `references/ProPgPassingArguments.html`

## Arrays

```freebasic
Dim arr(9) As Integer              ' 0 to 9
Dim arr2(1 To 10) As Integer       ' 1 to 10
Dim arr3(1 To 3, 1 To 3) As Double ' 2D array
Dim dynarr() As Integer            ' dynamic array
ReDim dynarr(19)                   ' resize dynamic array
ReDim Preserve dynarr(29)          ' resize preserving data
```

- `LBound(arr)` / `UBound(arr)` — get bounds
- `Erase arr` — erase/reset array
- Max 8 dimensions
- Row-major storage order

Reference: `references/CatPgArray.html`, `references/ProPgArrays.html`

## Operators

Arithmetic: `+`, `-`, `*`, `/`, `\` (integer div), `Mod`, `^` (power)
Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`
Logical: `And`, `Or`, `Xor`, `Not`, `Eqv`, `Imp`
Short-circuit: `AndAlso`, `OrElse`
String: `+` or `&` (concatenation)
Pointer: `@` (address), `*` (dereference), `->` (member access)
Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `\=`, `Mod=`, `^=`, `&=`, `Eqv=`, `Imp=`, `And=`, `Or=`, `Xor=`

Reference: `references/CatPgOperators.html`, `references/OpPrecedence.html`

## Pointers and Memory

```freebasic
Dim p As Integer Ptr = @variable     ' pointer to variable
Dim value As Integer = *p            ' dereference
Dim mem As Any Ptr = Allocate(100)   ' allocate memory
Deallocate(mem)                      ' free memory
```

- `Ptr` — pointer type modifier
- `@` / `VarPtr` — address-of operator
- `*` — dereference
- `Allocate`, `CAllocate`, `ReAllocate`, `Deallocate`
- `Peek` / `Poke` — direct memory access

Reference: `references/ProPgPointers.html`, `references/CatPgMemory.html`

## File I/O

```freebasic
' Sequential text
Open "file.txt" For Input As #1
Line Input #1, text$
Close #1

Open "file.txt" For Output As #1
Print #1, "Hello"
Close #1

' Binary
Open "file.bin" For Binary As #1
Put #1, , data
Get #1, , data
Close #1

' Random access
Open "file.dat" For Random As #1 Len = Len(MyType)
Put #1, record_number, mydata
Get #1, record_number, mydata
Close #1
```

Reference: `references/CatPgFile.html`, `references/ProPgFileIO.html`

## Object-Oriented Features

- `Type...End Type` with `Extends` for inheritance
- `Constructor` / `Destructor` for lifecycle management
- `Virtual` / `Abstract` / `Override` for polymorphism
- `Implements` for interface-like behavior
- `Property` with `Get`/`Set` accessors
- `Operator` overloading
- Access modifiers: `Public`, `Private`, `Protected`

Reference: `references/ProPgTypeObjects.html`, `references/ProPgPolymorphism.html`, `references/ProPgOperatorOverloading.html`

## Preprocessor

```freebasic
#define MACRO value
#ifdef SYMBOL
# ifndef SYMBOL
# else
# endif
#error "message"
#inclib "libraryname"
#include "file.bi"
```

Reference: `references/ProPgPreprocessor.html`, `references/CatPgPreProcess.html`

## Multithreading

```freebasic
Dim thread As Any Ptr = ThreadCreate(@MyThreadSub)
ThreadWait(thread)
MutexLock(mymutex)
MutexUnlock(mymutex)
```

- `ThreadCreate`, `ThreadWait`, `ThreadDetach`, `ThreadSelf`
- `MutexCreate`, `MutexDestroy`, `MutexLock`, `MutexUnlock`
- `CondCreate`, `CondDestroy`, `CondSignal`, `CondWait`, `CondBroadcast`

Reference: `references/CatPgThreading.html`, `references/ProPgMultiThreading.html`

## Graphics

FreeBASIC has a built-in 2D graphics library (fbgfx) and supports OpenGL.

```freebasic
ScreenRes 640, 480, 32
Line (x1, y1)-(x2, y2), color
Circle (cx, cy), radius, color
PSet (x, y), color
Draw String (x, y), "text"
```

Reference: `references/CatPgGfx.html`, `references/CatPgGfx2D.html`, `references/CatPgGfxScreen.html`

## Error Handling

- `On Error Goto label` — traditional error handling
- `Err` — error number
- `Erl` — error line
- `Error` — raise an error
- `Resume Next` / `Resume label`
- `Assert` / `AssertWarn` — debug assertions

Reference: `references/ProPgErrorHandling.html`, `references/CatPgError.html`

## Interfacing with C

- `Extern "C"` blocks for C-compatible linkage
- `#include` C header files
- `ByVal` / `ByRef` for argument passing to C functions
- `ZString Ptr` for C string interop
- `CDecl` calling convention

Reference: `references/TutInterfacingWithC.html`, `references/ProPgExternalFormats.html`

## Reference File Index

All documentation lives in `references/`. Key entry points:

| Topic | File |
|-------|------|
| Table of Contents | `references/DocToc.html` |
| Full Keyword Index (A-Z) | `references/CatPgFullIndex.html` |
| Keywords by Category | `references/CatPgFunctIndex.html` |
| Data Types | `references/TblVarTypes.html`, `references/CatPgStdDataTypes.html` |
| Variables | `references/CatPgVariables.html` |
| Control Flow | `references/CatPgControlFlow.html` |
| Procedures | `references/CatPgProcedures.html` |
| Arrays | `references/CatPgArray.html` |
| Strings | `references/CatPgString.html` |
| File I/O | `references/CatPgFile.html` |
| Math | `references/CatPgMath.html` |
| User Types / OOP | `references/CatPgUserDefTypes.html` |
| Operators | `references/CatPgOperators.html` |
| Pointers / Memory | `references/CatPgMemory.html`, `references/ProPgPointers.html` |
| Graphics | `references/CatPgGfx.html` |
| Threading | `references/CatPgThreading.html` |
| Preprocessor | `references/CatPgPreProcess.html` |
| Compiler Options | `references/CatPgCompOpt.html` |
| Tutorials | `references/CatPgProgrammer.html` |
| Error Handling | `references/ProPgErrorHandling.html` |
| C Interop | `references/TutInterfacingWithC.html` |

When generating FreeBASIC code, always prefer consulting the relevant reference file for accurate syntax. The HTML files contain official syntax, descriptions, examples, and dialect differences.
