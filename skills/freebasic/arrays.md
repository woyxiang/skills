For conditionals, see [control-flow.md](control-flow.md).
For functions, see [procedures.md](procedures.md).

# Arrays

## Declaration

```freebasic
' Fixed size
Dim arr(0 To 9) As Integer       ' 10 elements: arr(0) to arr(9)
Dim matrix(1 To 3, 1 To 3) As Double  ' 3x3 matrix

' Dynamic (with any)
Dim dynamic() As Integer
ReDim dynamic(0 To 9)

' With initial values
Dim data(3) As Integer => {1, 2, 3, 4}
```

## Array Functions

```freebasic
Dim arr(0 To 9) As Integer
LBound(arr)      ' returns 0 (lower bound)
UBound(arr)      ' returns 9 (upper bound)
ArrayLen(arr)    ' returns 10 (number of elements)
ArraySize(arr)   ' returns 40 (bytes)
```

## ReDim and Preserve

```freebasic
Dim arr() As Integer
ReDim arr(0 To 5)

ReDim Preserve arr(0 To 10)  ' preserve existing data
```

## Multi-dimensional Arrays

```freebasic
Dim grid(0 To 2, 0 To 2) As Integer  ' 3x3 grid
grid(0, 0) = 1
grid(1, 1) = 1

' 3D array
Dim cube(0 To 1, 0 To 1, 0 To 1) As Integer
```

## Array Descriptors

```freebasic
' Access internal array descriptor
#include "fbc-int/array.bi"
Dim pd As FBC.FBARRAY Ptr = FBC.ArrayDescriptorPtr(myArray())
```

## Static vs Dynamic

```freebasic
'$Static  ' default for fixed-size (stack allocated)
'$Dynamic ' force heap allocation

Dim static(100) As Integer    ' stack (or static)
Dim dynamic() As Integer
ReDim dynamic(1000) As Integer  ' heap
```

## Initializing Arrays

```freebasic
' Single dimension
Dim nums(2) As Integer => {10, 20, 30}

' Multi-dimension
Dim grid(1, 1) As Integer => {{1, 2}, {3, 4}}

' Erase clears array
Erase arr
```

## See Also

- [types.md](types.md) - Data types
- [procedures.md](procedures.md) - Passing arrays to functions
- [pointers.md](pointers.md) - Memory operations