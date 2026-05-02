For basic math, see [operators.md](operators.md).

# Mathematical Functions

## Basic Math

```freebasic
Abs(x)           ' absolute value
Sgn(x)           ' sign: -1, 0, or 1
Int(x)           ' floor (toward negative)
Fix(x)           ' truncate toward zero
Frac(x)          ' fractional part

Log(x)           ' natural log
Log10(x)         ' base 10 log
Exp(x)           ' e^x
```

## Trigonometry (angles in radians)

```freebasic
Sin(x)           ' sine
Cos(x)           ' cosine
Tan(x)           ' tangent
Asin(x)          ' arcsine
Acos(x)          ' arccosine
Atan(x)          ' arctangent
Atn(x)           ' alias for Atan

' Degrees to radians
Dim As Double rad = degrees * ATN(1) / 45
```

## Hyperbolic Functions

```freebasic
Sinh(x)          ' hyperbolic sine
Cosh(x)          ' hyperbolic cosine
Tanh(x)          ' hyperbolic tangent
```

## Power and Root

```freebasic
Sqr(x)           ' square root
x ^ y            ' exponentiation
Pow(x, y)        ' x^y (same as ^)
```

## Rounding

```freebasic
Round(x)         ' round to nearest integer
Round(x, n)      ' round to n decimal places
CInt(x)          ' round to Integer
CLng(x)          ' round to Long
```

## Constants

```freebasic
# define PI 3.14159265358979
# define E 2.71828182845905
```

## Random Numbers

```freebasic
Randomize Timer
Dim x As Single = Rnd()           ' 0 to 1
Dim i As Integer = Int(Rnd() * 10) ' 0 to 9

Randomize 123                      ' seed for reproducibility
```

## Number Conversions

```freebasic
Hex$(255)           ' "FF"
Bin$(255)           ' "11111111"
Oct$(255)           ' "377"
Str$(123)          ' "123"
Val("3.14")        ' 3.14
```

## Example

```freebasic
Dim As Double angle = 45 * ATN(1) / 45  ' 45 degrees in radians
Print "Sin(45): "; Sin(angle)
Print "Cos(45): "; Cos(angle)
Print "Sqr(2): "; Sqr(2)

' Circle area
Dim r As Double = 5
Print "Area: "; PI * r ^ 2
```

## See Also

- [operators.md](operators.md) - Arithmetic operators
- [types.md](types.md) - Numeric types
- [strings.md](strings.md) - Number formatting