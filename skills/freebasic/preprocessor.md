For conditional compilation, see [control-flow.md](control-flow.md).

# Preprocessor Directives

## Conditional Compilation

```freebasic
#if condition
    ' code
#elseif condition2
    ' code
#else
    ' code
#endif

#ifdef symbol
    ' code if symbol defined
#endif

#ifndef symbol
    ' code if symbol NOT defined
#endif
```

## Macro Definition

```freebasic
#define MAX_SIZE 100
#define PI 3.14159
#define INCREMENT(x) (x + 1)

' Type macro
#define MyType As Integer

' String macro
#define VERSION "1.0.0"
```

## Macro Procedures

```freebasic
#macro Assert(expr)
    #ifndef DEBUG
        Dim As Integer temp = 0
        If Not (expr) Then temp = 1 \ 0
    #endif
#endmacro

Assert(x > 0)
```

## Include Files

```freebasic
#include "header.bi"
#include "C:\path\to\file.bi"
#include "inc\constants.bi"

' Once-only include
#ifndef _MYHEADER_BI_
#define _MYHEADER_BI_

' ... declarations ...

#endif
```

## Library Linking

```freebasic
#inclib "gdi32"
#libpath "C:\windows\system32"

Declare Function GetDC Lib "user32" (ByVal hwnd As Any) As Long
```

## Pragmas

```freebasic
#pragma static
#pragma dynamic
#pragma opt level

' Reserve space
Dim shared buffer(1024) As Byte
#pragma reserve buffer, 1024
```

## Other Directives

```freebasic
#print "Compiling..."           ' print during compile
#error "Custom error message"   ' abort with error
#assert condition              ' assertion check

#line 100 "source.bas"          ' change line number / file
```

## Preprocessor Metacommands

```freebasic
'$Dynamic                     ' force dynamic arrays
'$Static                      ' force static arrays
'$Include "file.bi"           ' include file
'$If defined(symbol)          ' conditional
```

## Examples

```freebasic
' Version-specific code
#ifdef DEBUG
    Print "Debug mode"
#endif

' Platform detection
#ifdef __FB_DOS__
    Print "DOS platform"
#elseif __FB_LINUX__
    Print "Linux platform"
#elseif __FB_WIN32__
    Print "Windows platform"
#endif

' OS detection
#ifdef __FB_WIN32__
    #inclib "kernel32"
#endif
```

## See Also

- [control-flow.md](control-flow.md) - If/ElseIf/End If
- [compiler.md](compiler.md) - Compiler options
- [error-handling.md](error-handling.md) - Error handling