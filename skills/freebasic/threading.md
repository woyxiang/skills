For time functions, see [date-time.md](date-time.md).
For synchronization, see [error-handling.md](error-handling.md).

# Threading and Synchronization

## Creating Threads

```freebasic
Dim As Any Ptr handle

Sub MyThread(param As Any Ptr)
    Print "Thread running"
End Sub

handle = ThreadCreate(@MyThread)
ThreadWait(handle)
```

## ThreadCreate with Parameters

```freebasic
Dim shared counter As Integer

Sub ThreadFunc(param As Any Ptr)
    Dim As Integer count = *Cast(Integer Ptr, param)
    For i As Integer = 1 To count
        Print "Count: "; i
    Next
End Sub

Dim count As Integer = 10
Dim handle As Any Ptr = ThreadCreate(@ThreadFunc, @count)
ThreadWait(handle)
```

## Mutex

```freebasic
Dim mutex As Any Ptr

mutex = MutexCreate()
MutexLock(mutex)
    ' critical section
MutexUnlock(mutex)
MutexDestroy(mutex)
```

## Critical Sections

```freebasic
Dim cs As CRITICAL_SECTION

EnterCriticalSection(@cs)
    ' protected code
LeaveCriticalSection(@cs)
```

## Sleep and Wait

```freebasic
Sleep 1000              ' sleep 1 second
ThreadWait(handle)      ' wait for thread
```

## Thread Info

```freebasic
Dim id As Any Ptr = ThreadVar
' Thread-local storage
```

## Thread Example (Producer/Consumer)

```freebasic
Dim shared buffer(0 To 9) As Integer
Dim shared bufferIndex As Integer
Dim shared mutex As Any Ptr

Sub Producer()
    For i As Integer = 0 To 99
        MutexLock(mutex)
        buffer(bufferIndex Mod 10) = i
        bufferIndex += 1
        MutexUnlock(mutex)
        Sleep 1
    Next
End Sub

Sub Consumer()
    Dim sum As Integer
    Do While sum < 100
        MutexLock(mutex)
        If bufferIndex > 0 Then
            sum += 1
        End If
        MutexUnlock(mutex)
    Loop
End Sub

mutex = MutexCreate()
ThreadCreate(@Producer)
ThreadCreate(@Consumer)
```

## See Also

- [procedures.md](procedures.md) - Subroutines
- [basics.md](basics.md) - Console I/O
- [date-time.md](date-time.md) - Date/time functions