For variables, see [types.md](types.md).
For pointers, see [pointers.md](pointers.md).

# User-Defined Types (UDT)

## Basic Type Definition

```freebasic
Type Point
    x As Integer
    y As Integer
End Type

Dim p As Point
p.x = 10
p.y = 20
```

## With...End With

```freebasic
Dim p As Point
With p
    .x = 10
    .y = 20
End With
```

## Type with Methods

```freebasic
Type Circle
    x As Double
    y As Double
    r As Double

    Declare Sub Draw()
    Declare Function Area() As Double
End Type

Sub Circle.Draw()
    Circle (This.x, This.y), This.r
End Sub

Function Circle.Area() As Double
    Return 3.14159 * This.r * This.r
End Function
```

## Type Constructors

```freebasic
Type Vector
    x As Double
    y As Double

    Declare Constructor()
    Declare Constructor(ByVal _x As Double, ByVal _y As Double)
End Type

Constructor Vector()
    This.x = 0
    This.y = 0
End Constructor

Constructor Vector(ByVal _x As Double, ByVal _y As Double)
    This.x = _x
    This.y = _y
End Constructor
```

## Type Unions

```freebasic
Type Data
    union
        As Integer i
        As Byte b(0 To 3)
    End Union
End Type
```

## Enumerations

```freebasic
Enum Color
    Red = 1
    Green = 2
    Blue = 3
End Enum

Dim c As Color = Red
```

## Nested Types

```freebasic
Type Rectangle
    Type Edge
        x1 As Integer
        y1 As Integer
        x2 As Integer
        y2 As Integer
    End Type

    top As Edge
    bottom As Edge
End Type
```

## Type Aliases

```freebasic
Type String2 As String * 256
Dim s As String2
```

## See Also

- [types.md](types.md) - Basic data types
- [pointers.md](pointers.md) - Pointers to types
- [procedures.md](procedures.md) - Passing types to functions