For basic drawing, see [basics.md](basics.md).
For user input, see [basics.md](basics.md).

# Graphics Library

## Screen Modes

```freebasic
Screen 12           ' 640x480, 16 colors
Screen 13           ' 320x200, 256 colors
Screen 19           ' 640x480, 256 colors
Screen 20           ' 640x400, 256 colors

' 32-bit color
Screen 20, , , 640, 480, 32
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
Line (0, 0)-(100, 100), 4          ' draw line
Line (0, 0)-(100, 100), , B        ' rectangle (box)
Line (0, 0)-(100, 100), , BF       ' filled box

Circle (200, 200), 50, 12          ' circle outline
Circle (200, 200), 50, 12, , , , F ' filled circle

PSet (x, y), color                 ' set single pixel
Preset (x, y)                      ' set pixel to black

Draw String (x, y), "text", color  ' draw text at position
```

## Screen Information

```freebasic
ScreenInfo width, height, depth   ' get screen dimensions
Width 80, 30                       ' set text mode
```

## Double Buffering

```freebasic
Screen 20, , 2                    ' enable double buffer
' ... draw operations ...
Flip                               ' copy buffer to screen
Cls                                ' clear back buffer
```

## Images

```freebasic
Dim img As Any Ptr = ImageCreate(100, 100)  ' create image
BLoad "sprite.bmp", img                    ' load image
Put (x, y), img, PSet                      ' draw image
ImageDestroy(img)                          ' free memory
```

## User Input

```freebasic
' Keyboard
Dim As Integer key
key = GetKey$()
MultiKey(F1)                             ' check if F1 pressed

' Mouse
Dim mx As Integer, my As Integer, mb As Integer
GetMouse mx, my, mb
```

## Palette

```freebasic
Palette Get 0, r, g, b         ' get color
Palette Set 0, r, g, b         ' set color
Palette Using pal()            ' set multiple
```

## Viewport

```freebasic
View (0, 0)-(639, 479), , 7    ' set drawing area
Window (0, 0)-(639, 479)        ' coordinate system
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
- [procedures.md](procedures.md) - Organizing graphics code