For user-defined types, see [user-defined-types.md](user-defined-types.md).
For file I/O, see [file-io.md](file-io.md).

# Error Handling

FreeBASIC has two styles: **QB-style handlers** (`On Error Goto` / `Resume`) which need specific compiler settings, and **inline error checking** which works everywhere.

## Requirements for On Error / Resume

- `Resume` / `Resume Next` are only valid in `-lang deprecated`, `-lang fblite` or `-lang qb` (error 146 in `-lang fb`)
- `Resume` needs the `-ex` (or `-exx`) compiler switch; without it the program aborts with *runtime error 5 (illegal resume)*
- `On Error Goto` itself compiles in every dialect

## On Error Goto

```freebasic
#lang "fblite"

Sub ReadFile()
    Dim As Integer fn = FreeFile
    Open "data.txt" For Input As #fn

    On Error Goto ErrorHandler
    ' ... file operations ...
    Close #fn
    Exit Sub

ErrorHandler:
    Dim code As Long = Err()   ' save Err immediately, see gotcha below
    Print "Error "; code
    Resume Next
End Sub
```

Compile with `fbc -ex prog.bas`.

**Gotcha: `Err` is reset by internal functions.** Calling `Print` (or most runtime functions) after an error overwrites `Err` with its own status — `Print Err` often shows 0. Store it in a variable first: `code = Err()`.

## Err Function

```freebasic
Print Err()          ' last error number (Long) - or set it: Err = 1000
Print Erl()          ' line number where the error occurred
Print *Erfn()        ' name of the function where the error occurred
Print *Ermn()        ' name of the module where the error occurred
```

There is **no `Error$`** function (that is QB/VB): FreeBASIC has no built-in error-message string. Map codes to messages yourself, or use the runtime's own abort message.

`Err` can be read and written even without QB-style handlers. `Resume` resets it.

## Inline Error Checking (all dialects)

Procedures like `Open`, `Close`, `Kill`, `FileCopy` return an error code when used as functions — no `-e` switch needed:

```freebasic
Dim filename As String = "data.txt"
If Open(filename For Input As #1) <> 0 Then
    Print "could not open "; filename
End If
```

## Runtime Error Codes

FreeBASIC's codes are **not** the same as QB's:

| Code | Meaning | Code | Meaning |
|------|---------|------|---------|
| 0 | No error | 9 | Interrupted signal |
| 1 | Illegal function call | 10 | Illegal instruction signal |
| 2 | File not found | 11 | Floating point error signal |
| 3 | File I/O error | 12 | Segmentation violation signal |
| 4 | Out of memory | 13 | Termination request signal |
| 5 | Illegal resume | 14 | Abnormal termination signal |
| 6 | Out of bounds array access | 15 | Quit request signal |
| 7 | Null pointer access | 16 | Return without Gosub |
| 8 | No privileges | 17 | End of file |

There is no reserved user range: use high numbers (e.g. 1000+) for custom errors to avoid collisions.

## Custom Error Handling

```freebasic
#lang "fblite"

On Error Goto Handler
Error 1000            ' raise custom error number 1000
End

Handler:
Dim code As Long = Err()
Select Case code
    Case 2
        Print "File not found"
    Case Else
        Print "Error: "; code
End Select
Resume Next   ' continue after the failed statement
' Resume     ' ... or retry the failed statement
```

## Assert

```freebasic
Assert(x > 0)          ' halts with a message if false
AssertWarn(x > 0)      ' warns if false
```

`Assert`/`AssertWarn` are function-style macros — **parentheses are required**. They only take effect when compiled with `-g` or `-eassert`; otherwise they generate no code. Not available in `-lang qb` unless written `__ASSERT`.

## Cleanup

```freebasic
Sub SafeClose()
    On Error Goto 0  ' disable error handler
    Close #1
End Sub
```

## See Also

- [compiler.md](compiler.md) - The -e / -ex / -exx switches
- [file-io.md](file-io.md) - File operations
- [procedures.md](procedures.md) - Sub and Function
