import unittest
from math import sin, cos, tan, log, sqrt, pow, pi, e
from arival.prattparser import Parser


class TestArithmeticParser(unittest.TestCase):
    def parse(self, input):
        p = Parser()
        return p.parse(input)

    def testAdditionAndMultiplication(self):
        self.assertEqual(self.parse('2 + 3 * 4'), eval(compile('2 + 3 * 4', '<string>', 'eval')))

    def testNestedParentheses(self):
        self.assertEqual(self.parse('(5 - 2) * (8 + 3)'), eval(compile('(5 - 2) * (8 + 3)', '<string>', 'eval')))

    def testUnaryMinusAndMultiplication(self):
        self.assertEqual(self.parse('-7 + 4 * -2'), eval(compile('-7 + 4 * -2', '<string>', 'eval')))

    def testMaxFunctionAndTrigonometricOperations(self):
        self.assertEqual(self.parse('max(3, 7) - sqrt(9) * tan(45)'), eval(compile('max(3, 7) - sqrt(9) * tan(45)', '<string>', 'eval')))

    def testPowerOperatorAndTrigonometricFunction(self):
        self.assertEqual(self.parse('2 ^ 3 + cos(3.14) * 2.71'), eval(compile('2 ** 3 + cos(3.14) * 2.71', '<string>', 'eval')))

    def testMinFunctionAndLogarithmicOperations(self):
        self.assertEqual(self.parse('min(sqrt(16), log(4, 2)) / tan(30)'), eval(compile('min(sqrt(16), log(4, 2)) / tan(30)', '<string>', 'eval')))

    def testNegativeExponentAndSineFunction(self):
        self.assertEqual(self.parse('2 ^ -3 + sin(3.14/2)'), eval(compile('2 ** -3 + sin(3.14/2)', '<string>', 'eval')))

    def testDivisionAndMultiplication(self):
        self.assertEqual(self.parse('12 / 4 + 5 * 2 / 2'), eval(compile('12 / 4 + 5 * 2 / 2', '<string>', 'eval')))

    def testNestedFunctionsAndSubtraction(self):
        self.assertEqual(self.parse('max(min(2, 5), pow(3, sqrt(4))) - 1'), eval(compile('max(min(2, 5), pow(3, sqrt(4))) - 1', '<string>', 'eval')))

    def testPowerOperatorAndPowFunction(self):
        self.assertEqual(self.parse('2 ^ 3 + pow(4, 2)'), eval(compile('2 ** 3 + pow(4, 2)', '<string>', 'eval')))


    def test_mismatched_parentheses(self):
        with self.assertRaises(Exception):
            self.parse("(2 + 3 * 4")

    def test_unknown_operator(self):
        with self.assertRaises(Exception):
            self.parse("2 # 3")

    def test_missing_operand(self):
        with self.assertRaises(Exception):
            self.parse("2 +")

    def test_extra_operator(self):
        with self.assertRaises(Exception):
            self.parse("5 * 3 /")

    def test_mismatched_function_parentheses(self):
        with self.assertRaises(Exception):
            self.parse("min(2, 5 - pow(3, sqrt(4)")  # Mismatched parentheses

    def test_undefined_constant(self):
        with self.assertRaises(Exception):
            self.parse("pi + undefined_constant")

    def test_mismatched_nested_parentheses(self):
        with self.assertRaises(Exception):
            self.parse("min(2, 5 - pow(3, sqrt(4)) - 1")  # Mismatched parentheses

    # Add more test cases as needed...


if __name__ == '__main__':
    unittest.main()
