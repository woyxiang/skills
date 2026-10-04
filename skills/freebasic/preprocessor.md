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
#macro Check(expr)
    If (expr) = 0 Then Print "check failed: " + #expr
#endmacro

Dim As Integer x = 5
Check(x > 0)
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

Real options are `msbitfields`, `once`, `constness`, `lookup108` (plus `push`/`pop` to save and restore). There is no `#pragma static`/`dynamic`/`opt`/`reserve` - use `Option`s and `Dim`/`ReDim` instead.

```freebasic
#pragma once                    ' include-guard for this source file

#pragma push(constness, false)  ' silence "CONST qualifier discarded" warnings
' ... code ...
#pragma pop(constness)
```

## Other Directives

```freebasic
#print "Compiling..."           ' print during compile
#error "Custom error message"   ' abort with error
#assert 1 = 1                  ' compile-time assertion

#line 100 "source.bas"          ' change line number / file
```

## Preprocessor Metacommands

```freebasic
'$Dynamic                     ' force dynamic arrays
'$Static                      ' force static arrays
'$Include "file.bi"           ' include file

' Note: '$Dynamic/$Static/$Include are only in -lang fblite/qb
' and must be the first token on the line. There is no '$If - use #if.
```

## Examples

```freebasic
' Version-specific code
#ifdef DEBUG
    Print "Debug mode"
#endif

' Platform detection
#if defined(__FB_DOS__)
    Print "DOS platform"
#elseif defined(__FB_LINUX__)
    Print "Linux platform"
#elseif defined(__FB_WIN32__)
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