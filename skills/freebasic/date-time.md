For math functions, see [math.md](math.md).
For timing and delays in threads, see [threading.md](threading.md).

# Date and Time

Date/time serial functions (`Now`, `DateSerial`, `DatePart`, `DateAdd`, `DateDiff`, `Format`, ...) come from `#include once "vbcompat.bi"`. `Date$`, `Time$`, `Timer` and `Sleep` are built in.

Dates are **serial numbers**, not a data type: whole days since a reference date (`Long`), with a fractional time-of-day when created from `Now` or `TimeSerial` (`Double`). Use `Format` to turn a serial into a string.

## Current Date/Time

```freebasic
#include once "vbcompat.bi"

Print Date$              ' "05-02-2026" (MM-DD-YYYY)
Print Time$              ' "14:30:00" (HH:MM:SS)
Print Now                ' date+time serial (Double), local time
```

## DateSerial and TimeSerial

```freebasic
#include once "vbcompat.bi"

Dim ds As Long = DateSerial(2026, 5, 1)    ' date serial (whole days)
Dim ts As Double = TimeSerial(14, 30, 0)   ' time of day as a fraction
```

## DatePart

```freebasic
#include once "vbcompat.bi"

Print DatePart("yyyy", Now)   ' year
Print DatePart("m", Now)      ' month
Print DatePart("d", Now)      ' day
Print DatePart("h", Now)      ' hour
Print DatePart("n", Now)      ' minute
Print DatePart("s", Now)      ' second
```

## DateAdd and DateDiff

```freebasic
#include once "vbcompat.bi"

' both operate on date serials
Print Format(DateAdd("d", 7, Now), "yyyy-mm-dd")   ' one week from today
Dim days As Long = DateDiff("d", DateSerial(2026, 1, 1), Now)
```

## Timer

```freebasic
Dim startTime As Double = Timer
' ... code to measure ...
Dim elapsed As Double = Timer - startTime
```

## Sleep (time delay)

```freebasic
Sleep 1000              ' wait 1000 ms (1 second)
Sleep 1000, 1           ' 1 second, cannot be interrupted by a key press
Sleep                   ' wait until a key is pressed
```

Note: `Sleep amount` takes milliseconds in `-lang fb`/`fblite` but **seconds** in `-lang qb`. The two-argument form `Sleep amount, keyflag` is always milliseconds. `keyflag = 1` means the wait cannot be interrupted by a key press.

## Time Zones

`Now`, `Date$` and `Time$` return **local** time; there is no built-in UTC function. Use the OS API (e.g. `GetSystemTime` from `windows.bi`) when UTC is required.

## Formatting

`Format` accepts a date serial or a plain number plus a format string:

```freebasic
#include once "vbcompat.bi"

Print Format(Now, "yyyy-mm-dd")
Print Format(Now, "hh:nn:ss")
Print Format(Now, "mm/dd/yyyy hh:nn:ss")
Print Format(1234.5678, "0.00")   ' numeric formatting -> "1234.57"
```

## Example

```freebasic
#include once "vbcompat.bi"

Dim start As Double = Timer
For i As Integer = 1 To 1000
    ' some computation
Next
Dim elapsed As Double = Timer - start
Print "Elapsed time: "; elapsed; " seconds"

Print "Today is "; Format(Now, "yyyy-mm-dd")
Print "The time is "; Time$
```

## See Also

- [math.md](math.md) - Math functions
- [basics.md](basics.md) - Console I/O
- [threading.md](threading.md) - Thread timing
