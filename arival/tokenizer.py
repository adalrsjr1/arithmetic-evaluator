from __future__ import annotations
from collections import namedtuple
from enum import Enum

import re

class TokenType(str, Enum):
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    FUNCTION = 'FUNCTION',
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'
    EXPONENTIATION = '^'
    PARENTHESIS_LEFT = '('
    PARENTHESIS_RIGHT = ')'
    COMMA = ','

    def __str__(self):
        return self.name


FUNCTION_LIST: list[str] = [
    'sin',
    'cos',
    'tan',
    'pow',
    'sqrt',
    'log',
    'max',
    'min'
]

TOKEN_SPEC: list[tuple] = [
    (r'^\s+', None),
    (r'^(?:\d+(?:\.\s*\d*)?)', TokenType.NUMBER),
    (rf'^({'|'.join(FUNCTION_LIST)})', TokenType.FUNCTION),
    (r'^[A-Za-z_][A-Za-z0-9_]*', TokenType.IDENTIFIER),
    (r'^\+', TokenType.ADDITION),
    (r'^\-', TokenType.SUBTRACTION),
    (r'^\*', TokenType.MULTIPLICATION),
    (r'^\/', TokenType.DIVISION),
    (r'^\^', TokenType.EXPONENTIATION),
    (r'^\(', TokenType.PARENTHESIS_LEFT),
    (r'^\)', TokenType.PARENTHESIS_RIGHT),
    (r'^,', TokenType.COMMA)
]


class TokenizerError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


Token = namedtuple('Token', 'type value')
Token.is_function = lambda Token: Token.value in FUNCTION_LIST

class Tokenizer:
    def __init__(self, input: str):
        self.input: str = input
        self.cursor: int = 0

    def __iter__(self):
        # return Tokenizer(self.input)
        self.reset()
        return self

    def __next__(self):
        item = self.get_next_token()
        if item is None:
            raise StopIteration
        return item

    def reset(self):
        self.cursor = 0

    def has_more_tokens(self):
        return self.cursor < len(self.input)

    def match(self, regex: str, input_slice: str) -> str:
        matched = re.match(regex, input_slice)
        if matched is None:
            return None

        self.cursor += len(matched[0])
        return matched[0]

    def get_next_token(self) -> tuple[TokenType, str]:
        if not self.has_more_tokens():
            return None

        input_slice = self.input[self.cursor:]

        for regex, type in TOKEN_SPEC:
            token_value = self.match(regex, input_slice)

            # no rule was matched
            if token_value is None:
                continue

            # skip whitespace
            if type is None:
                return self.get_next_token()

            return Token(type, token_value)

        raise TokenizerError(f'unexpected token at pos {self.cursor}: \'{self.input_left_over()}\'')

    def input_left_over(self) -> str:
        return self.input[self.cursor:]
