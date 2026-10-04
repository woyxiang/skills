'' Starter: console program with input, a loop and a function.
'' Compile:  fbc -w all console-app.bas -x console-app

Function Add(ByVal a As Integer, ByVal b As Integer) As Integer
    Return a + b
End Function

Dim username As String
Print "What is your name? ";
Input username
Print "Hello, "; username; "!"

Dim total As Integer
For i As Integer = 1 To 5
    total = Add(total, i)
Next
Print "Sum of 1..5 = "; total

' Countdown loop, exit early on demand
Dim n As Integer = 10
Do While n > 0
    Print n;
    n -= 1
Loop
Print
Print "Done."
