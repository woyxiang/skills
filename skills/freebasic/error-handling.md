For user-defined types, see [user-defined-types.md](user-defined-types.md).
For pointers, see [pointers.md](pointers.md).

# Error Handling

## On Error Goto

```freebasic
Sub ReadFile()
    Dim As Integer fn = FreeFile
    Open "data.txt" For Input As #fn

    On Error Goto ErrorHandler

    ' ... file operations ...

    Close #fn
    Exit Sub

ErrorHandler:
    Print "Error "; Err; ": "; Error$
    Resume Next
End Sub
```

## Err Function

```freebasic
Print Err          ' last error code
Print Erl          ' line number
Print Error$        ' error message

If Err = 2 Then Print "File not found"
```

## Error Codes

| Code | Description |
|------|-------------|
| 2 | File not found |
| 3 | Path not found |
| 4 | Too many open files |
| 5 | Permission denied |
| 6 | Bad file number |
| 100 | End of file |

## Assert

```freebasic
Assert condition         ' abort if false
AssertWarn condition     ' warning if false
```

## Custom Error Handling

```freebasic
On Error Goto Handler

Open "missing.txt" For Input As #1

Handler:
Select Case Err
    Case 2
        Print "File not found"
    Case Else
        Print "Error: "; Error$
End Select

Resume Next  ' continue after error
Resume       ' retry failed statement
```

## Cleanup

```freebasic
Sub SafeClose()
    On Error Goto 0  ' disable error handler
    Close #1
End Sub
```

## See Also

- [procedures.md](procedures.md) - Sub and Function
- [file-io.md](file-io.md) - File operations
- [basics.md](basics.md) - Console I/O