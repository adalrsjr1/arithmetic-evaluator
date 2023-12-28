import math
import unittest

from prattparser import Parser, ParserError


class TestStatementParser(unittest.TestCase):
    runtime = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': -5,
            'x': math.pi,
            'y': 2 * math.pi,
        }
    
    def assertParser(self, input_str, expected):
        parser = Parser(TestStatementParser.runtime)
        
        self.assertEqual(parser.parse(input_str), float(expected))

    def testSimpleStatement(self):
        self.assertParser('2', 2)

    def testExample1(self):
        self.assertParser('5 - 2 - 1', 2)

    def testExample2(self):
        self.assertParser('12 / 2 / 3', 2)

    def testExample3(self):
        self.assertParser('1 + 2 * 3.0 - 4 / 2', 5.0)

    def testExample4(self):
        self.assertParser('2 ^ 2', 4)

    def testExample5(self):
        self.assertParser('2 ^ 2 ^ 3', 256)

    def testExample6(self):
        self.assertParser('9 ^ 0.5', 3.0)

    def testExample7(self):
        self.assertParser('(1 + 2) * 3', 9)

    def testExample8(self):
        self.assertParser('(2 ^ 2) ^ 3', 64)

    def testExample9(self):
        self.assertParser('-2', -2)

    def testExample10(self):
        self.assertParser('-2 + 3', 1)

    def testExample11(self):
        self.assertParser('-2 ^ 2 + 1', -3)

    def testExample12(self):
        self.assertParser('-(2 * 2)', -4)

    def testExample13(self):
        self.assertParser('- - 2)', 2)

    def testExample14(self):
        self.assertParser('- - - 2', -2)

    def testSinFunction(self):
        self.assertParser('sin(0)', 0)

    def testCosFunction(self):
        self.assertParser('cos(0)', 1)

    def testTanFunction(self):
        self.assertParser('tan(0)', 0)

    def testSqrtFunction(self):
        self.assertParser('sqrt(4)', 2)

    def testLogFunction(self):
        self.assertParser('log(100, 10)', math.log(100, 10))

    def testMaxFunction(self):
        self.assertParser('max(3, 7)', max(3, 7))

    def testMinFunction(self):
        self.assertParser('min(3, 7)', min(3, 7))

    def testInvalidNumber1(self):
        # Invalid number (missing digits after the dot)
        self.assertRaises(ParserError, self.assertParser, '2.  3', None)

    def testInvalidNumber2(self):
        # Invalid number (missing digits after the dot)
        self.assertParser('2.', 2)

    def testInvalidOperatorCombination(self):
        # Invalid operator combination
        self.assertRaises(ParserError, self.assertParser, '5 - * 2', None)

    def testMismatchedParentheses(self):
        # Mismatched parentheses
        self.assertRaises(ParserError, self.assertParser, '(1 + 2 * 3', None)

    def testUnknownFunction(self):
        # Unknown function
        self.assertRaises(ParserError, self.assertParser, 'unknown_function(2)', None)

    def testInvalidExponentiation(self):
        # Invalid exponentiation (missing base)
        self.assertRaises(ParserError, self.assertParser, '^ 2', None)

    def testInvalidLogFunction(self):
        # Invalid log function (missing base)
        self.assertRaises(ParserError, self.assertParser, 'log(100)', None)

    def testInvalidMaxFunction(self):
        # Invalid max function (missing arguments)
        self.assertRaises(ParserError, self.assertParser, 'max()', None)

    def testInvalidMinFunction(self):
        # Invalid min function (missing arguments)
        self.assertRaises(ParserError, self.assertParser, 'min()', None)

    def testVariableExpression1(self):
        # Single variable expression
        self.assertParser('x', eval('x', TestStatementParser.runtime))

    def testVariableExpression2(self):
        # Expression with addition and subtraction involving variables
        self.assertParser('a + b - c', eval('a + b - c', TestStatementParser.runtime))

    def testVariableExpression3(self):
        # Expression with multiplication and division involving variables
        self.assertParser('x * y / c', eval('x * y / c', TestStatementParser.runtime))

    def testVariableExpression4(self):
        # Expression with parentheses and variables
        self.assertParser('(a + b) * c', eval('(a + b) * c', TestStatementParser.runtime))

    def testVariableExpression5(self):
        # Expression with functions and variables
        self.assertParser('sin(x) + cos(y)', math.sin(TestStatementParser.runtime['x']) + math.cos(TestStatementParser.runtime['y']))

    def testVariableExpression6(self):
        # Complex expression with various operators and variables
        self.assertParser('2 * (a + b) / (c - d)', eval('2 * (a + b) / (c - d)', TestStatementParser.runtime))

    def testVariableExpression7(self):
        # Expression with variables and constants
        self.assertParser('a * 5 - b / 2', eval('a * 5 - b / 2', TestStatementParser.runtime))

    def testVariableExpression8(self):
        # Expression with exponentiation involving variables
        self.assertParser('x ^ 2', math.pi ** 2)

    def testVariableExpression9(self):
        # Expression with a mix of operators and variables
        self.assertParser('a * (b + c) - d / 2', eval('a * (b + c) - d / 2', TestStatementParser.runtime))

    def testInvalidExpressionNeverClosed(self):
        self.assertRaises(ParserError, self.assertParser, '(1 + 3', None)

    def testInvalidExpressionNeverOpened(self):
        self.assertRaises(ParserError, self.assertParser, '1 + 3) * 3', 12)

if __name__ == "__main__":
    unittest.main()