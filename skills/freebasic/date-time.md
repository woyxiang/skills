For time-related functions, see [date-time.md](date-time.md).

# Date and Time

## Current Date/Time

```freebasic
Print Date$              ' "05-02-2026" (MM-DD-YYYY)
Print Time$              ' "14:30:00" (HH:MM:SS)
Print Now                ' full date/time
```

## DateSerial and TimeSerial

```freebasic
Dim ds As Date = DateSerial(2026, 5, 1)
Dim ts As Double = TimeSerial(14, 30, 0)
```

## DatePart

```freebasic
Print DatePart("yyyy", Date$)   ' year
Print DatePart("m", Date$)      ' month
Print DatePart("d", Date$)      ' day
Print DatePart("h", Time$)      ' hour
Print DatePart("n", Time$)      ' minute
Print DatePart("s", Time$)      ' second
```

## DateAdd

```freebasic
Dim nextWeek As String = DateAdd("d", 7, Date$)
Dim nextMonth As String = DateAdd("m", 1, Date$)
```

## DateDiff

```freebasic
Dim days As Long = DateDiff("d", startDate$, endDate$)
```

## Timer

```freebasic
Dim startTime As Double = Timer
' ... code to measure ...
Dim elapsed As Double = Timer - startTime
```

## Sleep (time delay)

```freebasic
Sleep 1000              ' sleep 1000 ms (1 second)
Sleep 1000, 1           ' sleep 1 second (alternate syntax)
```

## Time Zones

```freebasic
' UTC time
Dim utc As Double = Now
```

## Formatting

```freebasic
' Date to string
Print Format(Now, "yyyy-mm-dd")
Print Format(Now, "hh:nn:ss")
Print Format(Now, "mm/dd/yyyy hh:nn:ss")
```

## Example

```freebasic
Dim start As Double = Timer
For i As Integer = 1 To 1000
    ' some computation
Next
Dim elapsed As Double = Timer - start
Print "Elapsed time: "; elapsed; " seconds"

Print "Today is "; Date$
Print "The time is "; Time$
```

## See Also

- [math.md](math.md) - Math functions
- [basics.md](basics.md) - Console I/O
- [operators.md](operators.md) - Time formatting with Format