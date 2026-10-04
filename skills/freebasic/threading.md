For time functions, see [date-time.md](date-time.md).
For error handling, see [error-handling.md](error-handling.md).

# Threading and Synchronization

Threading is not available in the `-lang qb` dialect. Thread procedures have the signature `Sub (ByVal userdata As Any Ptr)`; the handle and mutex types are `Any Ptr`.

## Creating Threads

```freebasic
Dim As Any Ptr handle

Sub MyThread(ByVal param As Any Ptr)
    Print "Thread running"
End Sub

handle = ThreadCreate(@MyThread)
ThreadWait(handle)
```

## ThreadCreate with Parameters

```freebasic
Dim Shared counter As Integer

Sub ThreadFunc(ByVal param As Any Ptr)
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

The portable synchronization primitive. A thread that calls `MutexLock` on a locked mutex waits until it is released.

```freebasic
Dim mutex As Any Ptr

mutex = MutexCreate()
MutexLock(mutex)
    ' critical section
MutexUnlock(mutex)
MutexDestroy(mutex)
```

## Critical Sections (Windows only)

`CRITICAL_SECTION` is a Win32 API type, not a FreeBASIC keyword — Windows only, needs `#include once "windows.bi"`. Portable code should use a Mutex instead.

```freebasic
#include once "windows.bi"

Dim cs As CRITICAL_SECTION
InitializeCriticalSection(@cs)
EnterCriticalSection(@cs)
    ' protected code
LeaveCriticalSection(@cs)
DeleteCriticalSection(@cs)
```

## Sleep and Wait

```freebasic
Sleep 1000              ' sleep 1 second (see date-time.md for dialect quirks)
ThreadWait(handle)      ' wait for a thread to finish
```

## Thread Identity

```freebasic
#include once "fbthread.bi"   ' ThreadSelf lives here

Sub Worker(ByVal param As Any Ptr)
    Print "my thread handle: "; ThreadSelf()
End Sub

Dim h As Any Ptr = ThreadCreate(@Worker)
ThreadWait(h)
```

`ThreadSelf()` returns the current thread's handle. FreeBASIC has no thread-local storage keyword: keep per-thread state in variables passed via the `param` pointer, or allocate per thread.

## Thread Example (Producer/Consumer)

```freebasic
Const MAXITEMS = 10

Dim Shared buffer(0 To MAXITEMS - 1) As Integer
Dim Shared count As Integer            ' items currently in the buffer
Dim Shared mutex As Any Ptr

Sub Producer(ByVal param As Any Ptr)
    For i As Integer = 1 To 20
        MutexLock(mutex)
        If count < MAXITEMS Then
            buffer(count) = i
            count += 1
        End If
        MutexUnlock(mutex)
        Sleep 1
    Next
End Sub

Sub Consumer(ByVal param As Any Ptr)
    Dim consumed As Integer
    Do While consumed < 20
        MutexLock(mutex)
        If count > 0 Then
            count -= 1
            consumed += 1
            Print "got "; buffer(count)
        End If
        MutexUnlock(mutex)
        Sleep 1
    Loop
End Sub

mutex = MutexCreate()
Dim p As Any Ptr = ThreadCreate(@Producer)
Dim c As Any Ptr = ThreadCreate(@Consumer)
ThreadWait(p)
ThreadWait(c)
MutexDestroy(mutex)
```

## See Also

- [procedures.md](procedures.md) - Subroutines
- [basics.md](basics.md) - Console I/O
- [date-time.md](date-time.md) - Date/time functions
