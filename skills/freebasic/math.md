For basic math, see [operators.md](operators.md).

# Mathematical Functions

All of these are built in; there is nothing to include.

## Basic Math

```freebasic
Dim As Double x = -3.5
Print Abs(x)           ' absolute value: 3.5
Print Sgn(x)           ' sign: -1, 0, or 1
Print Int(x)           ' floor (toward negative infinity): -4
Print Fix(x)           ' truncate toward zero: -3
Print Frac(x)          ' fractional part: -0.5
```

## Logarithms and Exponent

```freebasic
Dim As Double x = 2.7
Print Log(x)                ' natural log
Print Log(x) / Log(10)      ' base 10 log (no Log10 - compute it)
Print Exp(x)                ' e^x
```

## Trigonometry (angles in radians)

```freebasic
Dim As Double degrees = 45
Dim As Double rad = degrees * Atn(1) / 45   ' degrees to radians (Atn(1) = pi/4)

Print Sin(rad)          ' sine
Print Cos(rad)          ' cosine
Print Tan(rad)          ' tangent
Print Asin(0.5)         ' arcsine
Print Acos(0.5)         ' arccosine
Print Atn(1)            ' arctangent (not Atan!)
```

## Power and Root

```freebasic
Dim As Double x = 2, y = 10
Print Sqr(x)           ' square root
Print x ^ y            ' exponentiation (no Pow function - use ^)
```

## Rounding

There is no `Round` function - pick the behavior you want:

```freebasic
Dim As Double x = 2.7
Print CInt(x)          ' round to nearest (banker's rounding): 3
Print Fix(x)           ' truncate: 2
Print Int(x)           ' floor: 2
Print Int(x + 0.5)     ' round half up: 3
```

## Constants

```freebasic
#define PI 3.14159265358979
#define E 2.71828182845905
```

## Random Numbers

```freebasic
Randomize Timer
Dim As Single r = Rnd()            ' 0 to 1
Dim As Integer i = Int(Rnd() * 10) ' 0 to 9

Randomize 123                      ' seed for reproducibility
```

## Number Conversions

```freebasic
Print Hex$(255)           ' "FF"
Print Bin$(255)           ' "11111111"
Print Oct$(255)           ' "377"
Print Str$(123)           ' "123"
Print Val("3.14")         ' 3.14
```

## Example

```freebasic
#define PI 3.14159265358979

Dim As Double degrees = 45
Dim As Double angle = degrees * Atn(1) / 45   ' 45 degrees in radians
Print "Sin(45): "; Sin(angle)
Print "Cos(45): "; Cos(angle)
Print "Sqr(2): "; Sqr(2)

' Circle area
Dim As Double r = 5
Print "Area: "; PI * r ^ 2
```

## See Also

- [operators.md](operators.md) - Arithmetic operators
- [types.md](types.md) - Numeric types
