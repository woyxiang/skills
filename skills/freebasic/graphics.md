For console output, see [basics.md](basics.md).
For user input, see the User Input section below.

# Graphics Library

Graphics commands open a graphics screen via GfxLib (`Screen`/`ScreenRes`); most statements are not available in `-lang qb` (or need `__`-prefixed aliases there).

## Screen Modes

```freebasic
Screen 12            ' 640x480, 16 colors
Screen 13            ' 320x200, 256 colors
Screen 18, 32        ' 640x480, 32bpp depth

' custom resolution/depth/pages - the flexible form
ScreenRes 640, 480, 32
```

## Color

```freebasic
' Index color (0-255)
Color 12, 0          ' foreground, background

' 32-bit RGB
Dim As UInteger red = RGB(255, 0, 0)
Color , RGB(0, 0, 128)
```

## Drawing Commands

```freebasic
Dim As Integer x = 50, y = 60, col = 4

Line (0, 0)-(100, 100), col        ' draw line
Line (0, 0)-(100, 100), , B        ' rectangle (box)
Line (0, 0)-(100, 100), , BF       ' filled box

Circle (200, 200), 50, 12          ' circle outline
Circle (200, 200), 50, 12, , , , F ' filled circle

PSet (x, y), col                   ' set single pixel
Preset (x, y)                      ' set pixel to background color

Draw String (x, y), "text", col    ' draw text at position
```

## Screen Information

```freebasic
Dim As Integer w, h, d
ScreenInfo w, h, d                ' get screen dimensions (width/height/depth)
Width 80, 30                      ' set text mode size
```

## Double Buffering

```freebasic
Screen 20, , 2                    ' mode 20 with 2 pages
' ... draw operations ...
Flip                              ' copy buffer to screen
Cls                               ' clear back buffer
```

## Images

```freebasic
Dim As Integer x = 0, y = 0
Dim img As Any Ptr = ImageCreate(100, 100)  ' create image
BLoad "sprite.bmp", img                    ' load image
Put (x, y), img, PSet                      ' draw image
ImageDestroy(img)                          ' free memory
```

## User Input

```freebasic
' Keyboard
Dim As Integer k
k = GetKey()                               ' no $ suffix on GetKey

' Scancode constants (SC_F1, SC_LEFT, ...) live in fbgfx.bi,
' in the FB namespace when compiling in -lang fb
#include once "fbgfx.bi"
Using FB
If MultiKey(SC_F1) Then Print "F1 is held down"

' Mouse
Dim As Integer mx, my, mb
GetMouse mx, my, mb
```

## Palette

```freebasic
Dim As Integer r, g, b
Palette Get 0, r, g, b         ' get color

Dim pal(0 To 255) As UInteger
Palette Using pal(0)           ' set multiple (array element, not pal())
```

## Viewport

```freebasic
View (0, 0)-(639, 479), , 7    ' set drawing area
Window (0, 0)-(639, 479)       ' coordinate system
```

## Example

```freebasic
Screen 12
Color 15, 1

' Draw a house
Line (100, 200)-(300, 200), 15      ' base
Line (100, 200)-(100, 100), 15      ' left wall
Line (300, 200)-(300, 100), 15      ' right wall
Line (100, 100)-(200, 50), 15       ' roof left
Line (200, 50)-(300, 100), 15       ' roof right

' Window
Line (180, 130)-(220, 170), , BF    ' filled box

' Door
Line (230, 150)-(270, 200), 15, B

Sleep
```

## See Also

- [basics.md](basics.md) - Console I/O
- [date-time.md](date-time.md) - Sleep
