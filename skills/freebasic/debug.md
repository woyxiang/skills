For compiler options, see [compiler.md](compiler.md).
For error handling at runtime, see [error-handling.md](error-handling.md).

# Debugging and Gotchas

Every item here was verified against fbc 1.10.1. When in doubt, write a 5-line throwaway program and compile it instead of guessing.

## fbc Compile Errors

| Error | Meaning | Typical cause |
|-------|---------|---------------|
| 3 / 9: Expected End-of-Line / Expected expression | Syntax error | VB-ism that does not exist; missing `()` on `Assert`; keyword used as name |
| 4: Duplicated definition | Name already declared | Reused identifier case-insensitively (`I` vs `i`); name collides with a builtin |
| 14: Expected identifier | Reserved word used where a name is expected | `Dim x As Date`, `Dim byref As ...` |
| 42: Variable not declared | Unknown identifier | Missing `Dim`; function lives in a header (`Now`, `FileAttr`, `ThreadSelf`) |
| 61: Illegal inside functions | Module-level statement inside a `Sub`/`Function` | Nested `Sub` definitions; `#lang` inside a procedure |
| 146 / 147: Only valid in -lang deprecated or fblite or qb | Dialect-specific syntax | `Resume`, `DEFINT`, type suffixes, `ParamArray`, `'$Dynamic`, `Option Static` |
| 320: Reference not initialized | `ByRef` variable without initializer | `Dim ByRef r As Integer` - needs `= othervar` |
| 100: Division by zero | Constant folding found `x \ 0` | Macro "crash" tricks get evaluated at compile time |

## Words That Cannot Be Identifiers

The validator caught these in real doc examples - they parse as statements, not names:

`name`, `line`, `width`, `color`, `data`, `static`, `dynamic`, `view`, `ptr`, `byref`, `len`, `str`, `base`, `locate`, `screen`, `circle`, `point`

```freebasic
' Dim name As String    ' error 4: Duplicated definition - name is reserved
Dim username As String  ' fine
```

Type names are more forgiving: `Type Point` works as long as the type is defined before use. Variable names are not.

## VB/QB Functions That Do Not Exist in FreeBASIC

| You wrote | Reality |
|-----------|---------|
| `ParamArray args()` | No variadic parameters; pass an array `args() As Integer` |
| `CStr(x)` | `Str(x)` (or `Str(x, ...)` for formatting) |
| `Round(x, n)` | No `Round`; use `CInt` (banker's), `Fix`, or `Int(x + 0.5)` |
| `Pow(x, y)`, `x ** y` | The `^` operator |
| `Log10(x)` | `Log(x) / Log(10)` |
| `Atan(x)` | `Atn(x)` |
| `Sinh/Cosh/Tanh` | Not built in; derive from `Exp` |
| `Error$` | Does not exist; only `Err`, `Erl`, `Erfn`, `Ermn` |
| `Null` | Compare pointers against `0` |
| `ThreadVar` | Does not exist; `ThreadSelf()` returns the current handle |
| `CRITICAL_SECTION` | Win32 API; use `MutexCreate`/`MutexLock` (portable) |
| `ArrayLen`, `ArraySize` | `UBound(a) - LBound(a) + 1` |

## Functions Hidden Behind Headers

Calling these without the include gives "Variable not declared":

| Function | Include |
|----------|---------|
| `Now`, `DateSerial`, `DatePart`, `DateAdd`, `DateDiff`, `Format` | `vbcompat.bi` |
| `FileAttr` | `file.bi` (or `vbcompat.bi`) |
| `ThreadSelf` | `fbthread.bi` |
| `MultiKey` scancode constants (`SC_F1`, ...) | `fbgfx.bi` + `Using FB` (namespace in `-lang fb`) |

## Silent Surprises

**Integer is platform-sized.** On 64-bit targets `Integer` is 64-bit; `Long` is always 32-bit, `LongInt` always 64-bit. Use explicit types in APIs and file formats.

**CInt does banker's rounding.** `CInt(2.5) = 2` but `CInt(3.5) = 4` (round-half-to-even). Use `Int(x + 0.5)` for round-half-up.

**`Err` resets silently.** Internal functions like `Print` overwrite `Err` with their own status. Save it first: `code = Err()`.

**Operator precedence bites.** Verified: `-2 ^ 2 = -4`, `n And 1 <> 0` parses as `n And (1 <> 0)`, `n Shl 1 + 1` parses as `(n Shl 1) + 1`. Parenthesize.

**`Sleep` units change with dialect.** Milliseconds in `-lang fb`/`fblite`, seconds in `-lang qb`. The `Sleep amount, keyflag` form is always milliseconds.

**String indexing is 0-based, `Mid$` is 1-based.** `s[0]` is the first character code (97 for "abc"); `s[0] = 65` writes 'A'. `Mid$(s, 1, 1)` is the first character.

**`&` converts, `+` does not.** `"n=" + 5` is a type mismatch; `"n=" & 5` works.

**Overloads need the `Overload` keyword.** Two `Function Add` without `Overload` is "Duplicated definition".

**No lambdas.** `Dim f As Function(...)` + `f = @NamedFunction` is the idiom.

## Dialect Gates

Everything below is `-lang fblite`/`qb` only (error 146/147 in `-lang fb`):

- `Resume` / `Resume Next` (and `On Error` handlers that resume) - also need `-ex`
- `DEFINT`, `DIM x` without a type, type suffixes (`x%`, `s$`)
- `'$Dynamic` / `'$Static` / `Option Static` / `Option Dynamic`
- `ParamArray`-style declarations and `Screen , , page, page` swaps

## Syntax Traps

- `#lang "fb"` needs **quotes**; `#lang fb` is error 17
- `Assert(expr)` needs **parentheses** (it is a macro); without `-g`/`-eassert` it compiles to nothing
- `Open Lpt "LPT1:" As #1` takes a device name - there is no `Open Lpt For Output`
- `Seek #1, 1` (statement) vs `Seek(1)` (function, no `#`)
- `Palette Using pal(0)` - the array form takes an element, not `pal()`
- `Dim ByRef r As Integer = target` - ByRef locals must be initialized

## Verifying a Guess

```bash
printf 'Print CInt(2.5)\n' > /tmp/t.bas && fbc /tmp/t.bas -x /tmp/t && /tmp/t
```

A five-second compile beats a wrong answer. To scan all doc examples at once: `python scripts/validate-examples.py`.

## See Also

- [compiler.md](compiler.md) - Dialects and switches
- [error-handling.md](error-handling.md) - Runtime errors
- [types.md](types.md) - Data types
