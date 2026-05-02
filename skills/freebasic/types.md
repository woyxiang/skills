For variable declarations, see [basics.md](basics.md).
For operators, see [operators.md](operators.md).
For user-defined types, see [user-defined-types.md](user-defined-types.md).

# Data Types and Variables

## Primitive Types

| Type | Size | Range |
|------|------|-------|
| Byte | 1 byte | -128 to 127 |
| UByte | 1 byte | 0 to 255 |
| Short | 2 bytes | -32768 to 32767 |
| UShort | 2 bytes | 0 to 65535 |
| Integer | 4 bytes | -2147483648 to 2147483647 |
| UInteger | 4 bytes | 0 to 4294967295 |
| Long | 4 bytes | Same as Integer |
| ULong | 4 bytes | Same as UInteger |
| LongInt | 8 bytes | -9223372036854775808 to 9223372036854775807 |
| ULongInt | 8 bytes | 0 to 18446744073709551615 |
| Single | 4 bytes | ±1.5e-45 to ±3.4e38 |
| Double | 8 bytes | ±5.0e-324 to ±1.7e308 |

## Boolean
```freebasic
Dim As Boolean flag = True
flag = False
```

## String Types

```freebasic
Dim As String s = "Hello"        ' variable length
Dim As ZString * 256 z          ' fixed-size null-terminated
Dim As WString * 256 w          ' wide string (Unicode)
```

## Variable Declaration

```freebasic
Dim x As Integer          ' explicit type
Dim y As Double = 3.14    ' with initializer
Dim z                     ' implicit type (default Integer)
Var w = 123               ' Var infers type

' Multiple variables
Dim As Integer a, b, c
```

## Type Suffixes (QB compatibility)

```freebasic
Dim x%       ' Integer
Dim y!       ' Single
Dim z#       ' Double
Dim s$       ' String
Dim l&       ' Long
Dim sb%      ' Short
Dim ub%      ' UByte
```

## Variable Modifiers

```freebasic
Dim Shared x As Integer    ' global scope
Dim Static y As Integer     ' persists between calls
Dim Const PI As Double = 3.14159  ' constant
Dim ByRef r As Integer      ' reference to another variable
Dim As Integer Ptr p        ' pointer
```

## Type Casting

```freebasic
Dim x As Double = 3.14
Dim i As Integer = CInt(x)    ' convert to Integer
Dim s As String = Str$(i)     ' convert to string
Dim d As Double = Val("3.14") ' string to number
```

## Initialization Defaults

```freebasic
Dim As Integer x        ' 0
Dim As Double d         ' 0.0
Dim As String s         ' "" (empty)
Dim As Boolean b        ' False
Dim As Integer Ptr p    ' 0 (Null)
```

## Size and Length

```freebasic
Dim As Integer arr(0 To 9)
Print SizeOf(arr)      ' 40 bytes (10 * 4)
Print Len(s)           ' string length
```

## See Also

- [basics.md](basics.md) - Basic syntax and Hello World
- [operators.md](operators.md) - Arithmetic and comparison operators
- [user-defined-types.md](user-defined-types.md) - Type...End Type
- [pointers.md](pointers.md) - Pointers and memory
- [arrays.md](arrays.md) - Array declarations