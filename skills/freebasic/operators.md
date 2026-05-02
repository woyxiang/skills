For arithmetic operations, see [types.md](types.md).
For control flow, see [control-flow.md](control-flow.md).

# Operators and Expressions

## Arithmetic Operators

```freebasic
+    ' Addition
-    ' Subtraction
*    ' Multiplication
/    ' Division (floating point)
\    ' Integer division
Mod  ' Modulo (remainder)
^    ' Exponentiation
```

## Comparison Operators

```freebasic
=     ' Equal
<>    ' Not equal
<     ' Less than
>     ' Greater than
<=    ' Less than or equal
>=    ' Greater than or equal
```

## Logical Operators

```freebasic
And   ' Logical AND
Or    ' Logical OR
Not   ' Logical NOT
Xor   ' Exclusive OR
Imp   ' Implication
Eqv   ' Equivalence
```

## Bitwise Operators

```freebasic
And   ' Bitwise AND
Or    ' Bitwise OR
Not   ' Bitwise NOT
Xor   ' Bitwise XOR
Shl   ' Shift left
Shr   ' Shift right
```

## String Concatenation

```freebasic
"Hello " + "World"     ' returns "Hello World"
"Number: " & 42         ' returns "Number: 42"
```

## Assignment Operators

```freebasic
x = 10          ' simple assignment
x += 5          ' x = x + 5
x -= 3          ' x = x - 3
x *= 2          ' x = x * 2
x /= 4          ' x = x / 4
```

## Operator Precedence

1. Parentheses: `( )`
2. Exponentiation: `^`
3. Unary: `+`, `-`, `Not`
4. Multiplicative: `*`, `/`, `\`, `Mod`
5. Additive: `+`, `-`
6. Relational: `=`, `<>`, `<`, `>`, `<=`, `>=`
7. Logical: `And`, `Or`, `Xor`, `Imp`, `Eqv`

## Examples

```freebasic
Dim As Integer a = 10, b = 3
Print a + b     ' 13
Print a - b     ' 7
Print a * b     ' 30
Print a / b     ' 3.33333
Print a \ b     ' 3 (integer division)
Print a Mod b   ' 1 (remainder)
Print a ^ b     ' 1000

' Boolean
Dim As Boolean result = (a > 5) And (b < 10)
```

## Type Conversion

```freebasic
CInt()    ' to Integer
CLng()    ' to Long
CDbl()    ' to Double
CStr()    ' to String
CBool()   ' to Boolean
```

## See Also

- [types.md](types.md) - Data types
- [control-flow.md](control-flow.md) - If, For, While
- [strings.md](strings.md) - String operations