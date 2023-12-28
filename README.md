## Pratt Parser

This code implements a Python version of the [Pratt Parser
algorithm](https://en.wikipedia.org/wiki/Operator-precedence_parser#Pratt_parsing).

It is a variation of the code presented in [Nathan
Vaughn](https://inspirnathan.com/posts/164-pratt-parser-for-math-expressions-in-javascript)

In this version:
- parser support more math functions (`log`, `pow`, `sqrt`, `sin`, `cos`, `tan`,
  `max`, and `min`)
- resolve arbitrary variables like in `a + b / 3 * sin(2 * 3.14)`, where `a` and
  `b` are assigned in the parser runtime.

## Usage

```Python
parser = Parser()
print(parser.parse('1+2 * (pow(3,2) * sqrt(9))'))

>>> 81
```

When resolving variables, initialize the parser with a proper runtime:

```Python
runtime = {
    'a': 1,
    'b': 2,
    'c': 3
}

parser = Parser(runtime)
print(parser.parse('a+b * (pow(c,b) * sqrt(9))'))

>>> 81
```

## Extension

To add support to new math functions:

1. add the new function to  `tokenizer.FUNCTION_LIST`
2. edit `prattparser.Parser.fn` to resolve the new function add 

In case the new function has more than 2 arguments, the grammar must be edited
accordingly in the function `prattparser.Parser.fn_arg_expression`

## Roadmap

- [ ] add support to dynamic variables, e.g., `a + 1`, where `a` is an arbitrary
  function calling a DB:
  ```python
  def a ():
    db = connect()
    value = db.query(`select count(*) from my_table`)
    return float(value)
  ```

- [ ] add support to resolve dependent dynamic variables and identify cycles,
  e.g., `a + b + 1`:
```python
def a():
    return 3 + b()

def b():
    return 42 + a()

>>> Exception: Cycle identifyed when resolving variable [a]
```

- [ ] generate AST for lazy evaluation