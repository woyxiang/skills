'' Starter: read a text file, count lines/words/chars, write a report.
'' Compile:  fbc -w all file-report.bas -x file-report

Const FILENAME = "input.txt"

Dim As Integer lines, words, chars
Dim s As String

If Open(FILENAME For Input As #1) <> 0 Then
    Print "Cannot open "; FILENAME
    End 1
End If

Do Until EOF(1)
    Line Input #1, s
    lines += 1
    chars += Len(s)
    For i As Integer = 0 To Len(s) - 1
        If s[i] = 32 Then words += 1   ' count spaces as word separators
    Next
    words += 1
Loop
Close #1

Print "lines: "; lines
Print "words: "; words
Print "chars: "; chars
