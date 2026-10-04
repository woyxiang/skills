For conditionals, see [control-flow.md](control-flow.md).
For functions, see [procedures.md](procedures.md).

# Arrays

## Declaration

```freebasic
' Fixed size
Dim arr(0 To 9) As Integer       ' 10 elements: arr(0) to arr(9)
Dim matrix(1 To 3, 1 To 3) As Double  ' 3x3 matrix

' Dynamic (can be resized with ReDim)
Dim dyn() As Integer
ReDim dyn(0 To 9)

' With initial values
Dim values(3) As Integer => {1, 2, 3, 4}
```

## Array Functions

There are no `ArrayLen`/`ArraySize` functions - derive them from bounds:

```freebasic
Dim arr(0 To 9) As Integer
Print LBound(arr)                              ' 0 (lower bound)
Print UBound(arr)                              ' 9 (upper bound)
Print UBound(arr) - LBound(arr) + 1            ' 10 (number of elements)
Print (UBound(arr) - LBound(arr) + 1) * SizeOf(Integer)  ' size in bytes
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
Dim myArray(0 To 9) As Integer
Dim pd As FBC.FBARRAY Ptr = FBC.ArrayDescriptorPtr(myArray())
```

## Static vs Dynamic

In `-lang fb` a `Dim` with constant bounds is fixed-size and a `Dim arr()` resized with `ReDim` is dynamic - there is no switch to flip. `'$Static`/`'$Dynamic` and `Option Static`/`Option Dynamic` exist only in `-lang fblite`/`qb` (error 146 in `-lang fb`).

```freebasic
#lang "fblite"

'$Static                  ' fixed-size arrays by default
Dim st(100) As Integer

'$Dynamic                 ' heap-allocated arrays
Dim dyn() As Integer
ReDim dyn(1000) As Integer
```

## Initializing Arrays

```freebasic
' Single dimension
Dim nums(2) As Integer => {10, 20, 30}

' Multi-dimension
Dim grid(1, 1) As Integer => {{1, 2}, {3, 4}}

' Erase clears/reallocates
Dim arr(0 To 9) As Integer
Erase arr
```

## See Also

- [types.md](types.md) - Data types
- [procedures.md](procedures.md) - Passing arrays to functions
- [pointers.md](pointers.md) - Memory operations