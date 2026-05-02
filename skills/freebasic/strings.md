For string basics, see [basics.md](basics.md).
For string functions, see [strings.md](strings.md).

# String Functions

FreeBASIC provides rich string manipulation functions.

## Creating Strings

```freebasic
Dim As String s = "Hello"
Dim As ZString * 256 z = "Hello"    ' fixed-size null-terminated
Dim As WString * 256 w = "Hello"    ' wide string
```

## String Length

```freebasic
Dim s As String = "FreeBASIC"
Print Len(s)          ' 9
```

## Substring Extraction

```freebasic
Dim s As String = "FreeBASIC"
Left$(s, 4)           ' "Free"
Right$(s, 6)          ' "BASIC"
Mid$(s, 5, 4)         ' "BASIC" (from position 5, 4 chars)
Mid$(s, 5)            ' "BASIC" (from position 5 to end)
```

## Case Conversion

```freebasic
Dim s As String = "Hello"
LCase$(s)             ' "hello"
UCase$(s)             ' "HELLO"
```

## Searching

```freebasic
Dim s As String = "FreeBASIC"
InStr(s, "BAS")       ' returns 5 (position of "BAS")
InStrRev(s, "A")      ' returns 9 (last occurrence)
```

## Trimming

```freebasic
Dim s As String = "  hello  "
LTrim$(s)             ' "hello  "
RTrim$(s)             ' "  hello"
Trim$(s)              ' "hello"
```

## String Conversion

```freebasic
Str$(123)             ' "123" (number to string)
Val("456")            ' 456 (string to number)
Hex$(255)             ' "FF" (to hex)
Bin$(255)             ' "11111111" (to binary)
Oct$(255)             ' "377" (to octal)
```

## Character Functions

```freebasic
Chr$(65)              ' "A" (ASCII code to character)
Asc("A")              ' 65 (character to ASCII)
```

## String Building

```freebasic
String$(10, "*")      ' "**********"
Space$(10)            ' "          "
```

## Replacing

```freebasic
' Using Mid statement
Dim s As String = "Hello World"
Mid$(s, 7) = "Universe"  ' "Hello Universe"
```

## String Comparison

```freebasic
If s1 = s2 Then Print "Equal"
If s1 < s2 Then Print "s1 < s2"
```

## See Also

- [basics.md](basics.md) - Print, Input
- [operators.md](operators.md) - String concatenation
- [file-io.md](file-io.md) - Reading/writing strings to files