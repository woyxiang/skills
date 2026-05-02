For memory allocation, see [arrays.md](arrays.md).
For types, see [user-defined-types.md](user-defined-types.md).

# Pointers and Memory

## Pointer Declaration

```freebasic
Dim p As Integer Ptr
Dim s As String Ptr
Dim byref As Integer Ptr  ' same as Integer Ptr
```

## AddressOf

```freebasic
Dim x As Integer = 10
Dim p As Integer Ptr = @x    ' get address of x
Print *p                     ' dereference: 10
```

## Memory Allocation

```freebasic
Dim p As Integer Ptr

' Allocate
p = Allocate(100)           ' allocate 100 bytes

' Reallocate
p = Reallocate(p, 200)      ' resize

' Deallocate
Deallocate(p)               ' free memory
p = 0                        ' set to NULL
```

## Null Pointer

```freebasic
Dim p As Integer Ptr = 0
If p = 0 Then Print "Pointer is NULL"
If p = Null Then Print "NULL pointer"
```

## Pointer Arithmetic

```freebasic
Dim arr(0 To 9) As Integer
Dim p As Integer Ptr = @arr(0)

p += 1          ' move to next element
p -= 1          ' move to previous
*p = 100        ' set value at pointer

' Array indexing via pointer
Dim p2 As Integer Ptr = @arr(0)
For i As Integer = 0 To 9
    Print p2[i]    ' same as *(p2 + i)
Next
```

## Function Pointers

```freebasic
Type CompareFunc As Function(ByVal As Integer, ByVal As Integer) As Integer

Dim cmp As CompareFunc
cmp = @MyCompare

result = cmp(a, b)
```

## Typedef

```freebasic
Type IntegerPtr As Integer Ptr
Dim p As IntegerPtr
```

## Dereference Operator

```freebasic
Dim x As Integer = 10
Dim p As Integer Ptr = @x
*p = 20                  ' modify x through pointer
Print x                  ' 20
```

## Pointer to Pointer

```freebasic
Dim x As Integer = 10
Dim p As Integer Ptr = @x
Dim pp As Integer Ptr Ptr = @p
**pp = 30               ' x = 30
```

## SizeOf with Pointers

```freebasic
Print SizeOf(Integer Ptr)    ' usually 4 or 8 bytes
```

## Common Patterns

```freebasic
' String to ZString conversion
Dim s As String = "Hello"
Dim z As ZString Ptr = StrPtr(s)

' UDT pointer
Type Point
    x As Integer
    y As Integer
End Type

Dim p As Point Ptr = Allocate(SizeOf(Point))
p->x = 10
p->y = 20
Deallocate(p)
```

## See Also

- [types.md](types.md) - Basic types
- [user-defined-types.md](user-defined-types.md) - UDT pointers
- [procedures.md](procedures.md) - Function pointers