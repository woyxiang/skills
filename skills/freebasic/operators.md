For arithmetic operations, see [types.md](types.md).
For control flow, see [control-flow.md](control-flow.md).

# Operators and Expressions

## Arithmetic Operators

| Op | Description |
|----|-------------|
| `+` `-` | Addition, subtraction |
| `*` `/` | Multiply, floating-point divide |
| `\` | Integer division (truncates) |
| `Mod` | Modulo (remainder) |
| `^` | Exponentiation |

## Comparison Operators

| Op | Description |
|----|-------------|
| `=` `<>` | Equal, not equal |
| `<` `>` | Less than, greater than |
| `<=` `>=` | Less/greater or equal |

Comparison expressions evaluate to `-1` (true) or `0` (false).

## Logical and Bitwise Operators

Integer operands are treated bitwise; Boolean operands logically.

| Op | Description |
|----|-------------|
| `Not` | Complement / logical NOT |
| `And` | Conjunction / bitwise AND |
| `Or` | Inclusive disjunction / bitwise OR |
| `Xor` | Exclusive or |
| `Eqv` | Equivalence |
| `Imp` | Implication |
| `AndAlso` / `OrElse` | Short-circuit And / Or |
| `Shl` `Shr` | Shift left / right |

## String Concatenation

```freebasic
Dim result As String
result = "Hello " + "World"       ' both operands String
result = "Number: " & 42          ' & converts numbers to strings
```

## Assignment Operators

```freebasic
Dim As Integer x = 10
x += 5          ' x = x + 5
x -= 3          ' x = x - 3
x *= 2          ' x = x * 2
x /= 4          ' x = x / 4
x Mod= 3        ' x = x Mod 3
x Shl= 1        ' x = x Shl 1
```

## Operator Precedence

Simplified, highest first (full table in the manual, `OpPrecedence.html`):

1. Function-like: `Cast`, `StrPtr`, `VarPtr`, `ProcPtr`
2. Indexing/calls/member access: `[]`, `()`, `.`, `->`
3. Pointers: `@`, `*` (deref), `New`, `Delete`
4. `^`
5. unary `-` (negation)
6. `*`, `/`, `\`, `Mod`, `Shl`, `Shr`
7. `+`, `-`, `&`, `Is`
8. Comparisons: `=`, `<>`, `<`, `<=`, `>=`, `>`
9. `Not`
10. `And`, then `Or`, `Eqv`, `Imp`, `Xor`, `AndAlso`, `OrElse`
11. Assignment operators

Surprises from this order — use parentheses:

```freebasic
Dim n As Integer = 3
Print -2 ^ 2              ' -4, NOT 4: ^ binds tighter than unary minus
Print n And 1 <> 0        ' And (1 <> 0), NOT (n And 1) <> 0
Print n Shl 1 + 1         ' (n Shl 1) + 1, NOT n Shl (1 + 1)
```

## Type Conversion

```freebasic
Dim As Double d = 1.5
Print CInt(d)     ' to Integer (rounded)
Print CLng(d)     ' to Long
Print CDbl("3.14")' to Double
Print Str(d)      ' to String (there is no CStr - that is VB)
Print CBool(d)    ' to Boolean
```

## See Also

- [types.md](types.md) - Data types
- [control-flow.md](control-flow.md) - If, For, While
