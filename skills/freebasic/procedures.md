For variables, see [types.md](types.md).
For control flow, see [control-flow.md](control-flow.md).

# Procedures (Functions and Subs)

## Function

```freebasic
Function Add(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Dim result As Integer = Add(3, 4)  ' 7
```

## Sub

```freebasic
Sub SayHello(msg As String)
    Print "Hello, " + msg + "!"
End Sub

SayHello("World")
```

## Parameters

```freebasic
' ByVal (pass by value - copy)
Sub ProcByVal(ByVal x As Integer)
    x = 100  ' only affects local copy
End Sub

' ByRef (pass by reference - original)
Sub ProcByRef(ByRef x As Integer)
    x = 100  ' modifies original
End Sub

' Optional parameters
Sub ProcOpt(ByVal x As Integer = 0)
    Print x
End Sub

' Variable number of arguments: pass an array
' (FreeBASIC has no ParamArray - that is VB)
Sub PrintAll(args() As Integer)
    For i As Integer = 0 To Ubound(args)
        Print args(i)
    Next
End Sub
```

## Overloading

```freebasic
' Multiple functions with same name: mark each with Overload
Function Add Overload (ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Function Add Overload (ByVal a As Double, ByVal b As Double) As Double
    Return a + b
End Function
```

## Calling Conventions

```freebasic
' Default is stdcall (cdecl for variadic)
Declare Sub Proc Lib "mylib" Alias "proc" (ByVal x As Integer)

' Explicit calling convention
Declare Sub ProcCDecl CDecl (ByVal x As Integer)
Declare Sub ProcStdCall StdCall (ByVal x As Integer)
Declare Sub ProcPascal Pascal (ByVal x As Integer)
```

## Return Values

```freebasic
' Using Return
Function Factorial(n As Integer) As LongInt
    If n <= 1 Then Return 1
    Return n * Factorial(n - 1)
End Function

' Using function name (older style)
Function Max(a As Integer, b As Integer) As Integer
    If a > b Then
        Max = a
    Else
        Max = b
    End If
End Function
```

## Public and Private

```freebasic
Public Sub GlobalProc()
    Print "Visible everywhere"
End Sub

Private Sub LocalProc()
    Print "Only in this module"
End Sub
```

## Lambda / Inline Functions

```freebasic
' FreeBASIC has no lambdas - use a named function and its address
Function Add(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Dim fn As Function(ByVal As Integer, ByVal As Integer) As Integer
fn = @Add
Print fn(2, 3)   ' 5
```

## See Also

- [types.md](types.md) - Basic types
- [control-flow.md](control-flow.md) - Return statement
- [arrays.md](arrays.md) - Passing arrays to procedures
- [pointers.md](pointers.md) - Function pointers