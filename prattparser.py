# Pratt Parser algorithm
#
# Inspired by:
# https://inspirnathan.com/posts/164-pratt-parser-for-math-expressions-in-javascript/
#
# This version:
#   - resolves any arbitray variable defined int the parser runtime
#   - resolves more math functions as depicted in the `grammar` file
#
# The project is under MIT License
#
# Author: Adalberto R. Sampaio Jr (@adalrsjr1) [2023]

import math

from tokenizer import Token, Tokenizer, TokenType


class ParserError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class Parser:
    """
    The parser implements the Pratt algorithm to evaluate math expressions.

    To result arbitrary variables in the expression, the `Parser` class must be
    initialized with the `runtime` argument (a dictionary mapping the variable
    name and its assigned value).

    To use the parser, pass the string of the math expression to the parse
    function.

    The Parse evaluates the following operations and math functions:
        - basic operators: `+, -, *, /`
        - power operator: `^`
        - basic trig functions: `sin, cos, tan`
        - power functions (same python signature): `log, sqrt, pow`
        - `max, min`

    Next is a valid example of math expression for this parser. Check the `test`
    folder for more examples:
        ```
        5 * (sqrt(9) + sin(2 * 3.14)) - x / 2
        # runtime{'x': 10}
        ```
    """
    def __init__(self, runtime: dict[str, float] = {}):
        self.runtime = runtime

    def parse(self, input: str):
        self.input: str = input
        self.tokenizer: Tokenizer = Tokenizer(input)
        self.lookahead: Token = self.tokenizer.get_next_token()

        self.operators = {
            '^': 5,
            # a unary operation (-) technically has higher precedence than multiplication/division
            # but lower precedence than exponentiation.
            'unary': 4,
            '*': 3,
            '/': 3,
            '+': 2,
            '-': 2,
        }

        result = self.expression()

        if self.tokenizer.has_more_tokens():
            raise ParserError(f'parser cannot process the entire expression, error before pos [{self.tokenizer.cursor}]'
                              f' leftover: [{self.tokenizer.input_left_over()}]')
        return result

    # expect a particular token, consume it, and move to the next token
    def consume(self, token_type: TokenType) -> Token:
        token = self.lookahead

        if token is None:
            raise ParserError(f'unexpected end of input at pos [{self.tokenizer.cursor}], expected {token_type}')

        if token.type != token_type:
            raise ParserError(f'unexpected token: [{token.type}], expected [{token_type}]')

        # advance to the next token
        self.lookahead = self.tokenizer.get_next_token()

        return token

    def get_precedence(self, token: Token) -> int:
        if token == 'unary':
            return self.operators.get('unary')

        if token and token.type:
            return self.operators.get(token.value, 0)

        return 0

    ###
    # Expression
    #   = Prefix (Infix)*
    ###
    def expression(self, precedence: int = 0) -> any:
        left = self.prefix()

        while precedence < self.get_precedence(self.lookahead):
            left = self.infix(left, self.lookahead.type)

        return left

    ###
    # Prefix
    #   = ParenthesizedExpression
    #   | UnaryExpression
    #   | FunctionExpression
    #   | VarExpression
    #   | NUMBER
    ###
    def prefix(self) -> any:
        if self.lookahead.type == TokenType.PARENTHESIS_LEFT:
            return self.parenthesized_expression()

        if self.lookahead.type == TokenType.SUBTRACTION:
            return self.unary_expression()

        if self.lookahead.type == TokenType.FUNCTION:
            return self.function_expression()

        if self.lookahead.type == TokenType.IDENTIFIER:
            return self.var_expression()

        token = self.consume(TokenType.NUMBER)
        try:
            return float(token.value)
        except ValueError:
            raise ParserError(f'cannot convert {token.value} into a valid number')

    ###
    # Infix
    #   = ("+" / "-" / "*" / "/" / "^") Expression
    ###
    def infix(self, left, operator_type: TokenType) -> any:
        token = self.consume(operator_type)
        new_precedence = self.operators[token.value]  # new precedence we pass to the "Expression" method
        if token.type == TokenType.ADDITION:
            return left + self.expression(new_precedence)
        elif token.type == TokenType.SUBTRACTION:
            return left - self.expression(new_precedence)
        elif token.type == TokenType.MULTIPLICATION:
            return left * self.expression(new_precedence)
        elif token.type == TokenType.DIVISION:
            return left / self.expression(new_precedence)
        elif token.type == TokenType.EXPONENTIATION:
            # exponentiation has right-associativity, this means 2^2^3 = 256
            # thus, we need to subtract one from a precedence we pass into the
            # Expression method.
            return left ** self.expression(new_precedence - 1)

    ###
    # ParenthesizedExpression
    #   = "(" Expression ")"
    ###
    def parenthesized_expression(self) -> any:
        self.consume(TokenType.PARENTHESIS_LEFT)
        expression = self.expression()
        self.consume(TokenType.PARENTHESIS_RIGHT)
        return expression

    ###
    # UnaryExpression
    #   = "-" Expression
    ###
    def unary_expression(self) -> any:
        self.consume(TokenType.SUBTRACTION)
        return -self.expression(self.get_precedence('unary'))

    # VarExpression
    #   = IDENTIFIER
    def var_expression(self) -> any:
        id = self.consume(TokenType.IDENTIFIER).value
        try:
            return self.runtime[id]
        except KeyError:
            raise ParserError(f'cannot resolve variable [{id}]')

    ###
    # FunctionExpression
    #   = FUNCTION ParenthesizedExpression
    ###
    def function_expression(self) -> any:
        id = self.consume(TokenType.FUNCTION).value
        expressions = self.fn_arg_expression()
        return self.fn(id, expressions)

    ###
    # FnArgExpression
    #   = "(" Expression ")"
    #   | "(" Expression "," Expression ")"
    ###
    def fn_arg_expression(self) -> any:
        expressions = []
        self.consume(TokenType.PARENTHESIS_LEFT)
        expressions.append(self.expression())

        if self.lookahead.type == TokenType.COMMA:
            self.consume(TokenType.COMMA)
            expressions.append(self.expression())

        self.consume(TokenType.PARENTHESIS_RIGHT)
        return expressions

    # when adding support to new methods, also edit the tokenizer
    # function list
    def fn(self, id: str, value: list[str]):
        try:
            if id == 'sin':
                return math.sin(value[0])
            elif id == 'cos':
                return math.cos(value[0])
            elif id == 'tan':
                return math.tan(value[0])
            elif id == 'sqrt':
                return math.sqrt(value[0])
            elif id == 'log':
                return math.log(value[0], value[1])
            elif id == 'pow':
                return math.pow(value[0], value[1])
            elif id == 'max':
                return max(value[0], value[1])
            elif id == 'min':
                return min(value[0], value[1])
            else:
                raise ParserError(f'ivalid operation: {id}')
        except IndexError:
            raise ParserError(f'function [{id}] received wrong number of parameters [{len(value)}]')
