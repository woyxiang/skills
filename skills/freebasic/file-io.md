For file basics, see [basics.md](basics.md).
For console I/O, see [basics.md](basics.md).

# File I/O

## Opening Files

```freebasic
' Open for output (write)
Open "file.txt" For Output As #1

' Open for input (read)
Open "file.txt" For Input As #1

' Open for append
Open "file.txt" For Append As #1

' Open for binary
Open "file.txt" For Binary As #1
```

## Closing Files

```freebasic
Close #1        ' close single file
Close #1, #2    ' close multiple
Close           ' close all files
```

## File Numbers

```freebasic
Dim f As Integer = FreeFile()  ' get next available file number
Open "data.txt" For Output As #f
```

## Writing to Files

```freebasic
Print #1, "Hello"           ' write line with newline
Print #1, "Value: "; x       ' with variable
Write #1, data1, data2       ' binary-style write
```

## Reading from Files

```freebasic
Dim line As String
Input #1, line                ' read until comma or newline
Line Input #1, line           ' read entire line
```

## Binary I/O

```freebasic
Dim As Integer x, y
Get #1, , x                   ' read single value
Put #1, , x                   ' write single value
Get #1, 100, x               ' read at position
Put #1, 100, x               ' write at position
```

## File Position

```freebasic
Seek #1, 1                   ' move to beginning
Seek(#1)                     ' get current position
EOF(1)                       ' check end of file
LOF(1)                       ' length of file
FileAttr(1)                  ' file mode
```

## Examples

```freebasic
' Write data
Dim f As Integer = FreeFile()
Open "data.bin" For Binary As #f
Dim As Integer age = 25
Dim As Double salary = 50000.0
Put #f, , age
Put #f, , salary
Close #f

' Read data
Open "data.bin" For Binary As #f
Get #f, , age
Get #f, , salary
Close #f

' Text file
Dim f As Integer = FreeFile()
Open "log.txt" For Append As #f
Print #f, "Log entry: "; Now
Close #f
```

## Console as File

```freebasic
Open Cons For Input As #1    ' stdin
Open Cons For Output As #1   ' stdout
Open Err For Input As #1     ' stderr
Open Lpt For Output As #1    ' printer
```

## See Also

- [basics.md](basics.md) - Console Print/Input
- [date-time.md](date-time.md) - Date/time functions
- [strings.md](strings.md) - String manipulation