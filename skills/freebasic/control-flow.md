For conditionals, see [control-flow.md](control-flow.md).
For loops, see [control-flow.md](control-flow.md).

# Control Flow

## If...Then...Else

```freebasic
If x > 0 Then
    Print "positive"
ElseIf x < 0 Then
    Print "negative"
Else
    Print "zero"
End If

' Single line
If x > 0 Then Print "positive"
```

## Select Case

```freebasic
Select Case grade
    Case Is >= 90
        Print "A"
    Case 80 To 89
        Print "B"
    Case 70 To 79
        Print "C"
    Case Else
        Print "F"
End Select
```

## For...Next

```freebasic
For i As Integer = 1 To 10
    Print i
Next

' With step
For i As Integer = 10 To 1 Step -1
    Print i
Next

' Loop variable scope
For i As Integer = 1 To 5 : Print i; : Next
```

## While...Wend

```freebasic
While count < 10
    Print count
    count += 1
Wend
```

## Do...Loop

```freebasic
Do While condition
    ' ...
Loop

Do Until condition
    ' ...
Loop

Do
    ' ...
Loop While condition

Do
    ' ...
Loop Until condition
```

## Continue and Exit

```freebasic
For i = 1 To 10
    If i = 5 Then Continue For  ' skip to next iteration
    If i = 8 Then Exit For      ' exit loop early
    Print i
Next

Do While True
    If someCondition Then Exit Do
Loop
```

## Goto (discouraged)

```freebasic
Goto label

Label:
Print "After goto"
```

## See Also

- [procedures.md](procedures.md) - Exiting procedures early
- [error-handling.md](error-handling.md) - Error handling
- [basics.md](basics.md) - Basic I/O