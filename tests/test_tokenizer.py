import unittest
from tokenizer import Tokenizer, TokenizerError

class TestStatementTokenization(unittest.TestCase):

    def assertTokenization(self, input_str, expected_tokens):
        tokenizer = Tokenizer(input_str)
        for token in tokenizer:
            pass

        self.assertEqual(len(input_str), tokenizer.cursor, f'cannot tokenize whole input, leftover: {tokenizer.input_left_over()}')

    def testValidStatement1(self):
        self.assertTokenization('10 + 20 * 30 - 40', '')


    def testValidStatements1(self):
        self.assertTokenization("2 + 3 * log(10) - pi^2", ['2', '+', '3', '*', 'log', '(', '10', ')', '-', 'pi', '^', '2'])

    def testValidStatements2(self):
        self.assertTokenization("min(max(1, 5), sqrt(4)) * 3 / e", ['min', '(', 'max', '(', '1', ',', '5', ')', ',', 'sqrt', '(', '4', ')', ')', '*', '3', '/', 'e'])

    def testStatementsWithIdentifiers(self):
        self.assertTokenization("variable1 + variable_2 * 5", ['variable1', '+', 'variable_2', '*', '5'])

    def testStatementsWithNumbersAndConstants(self):
        self.assertTokenization("3.14 * pi + e^2", ['3.14', '*', 'pi', '+', 'e', '^', '2'])

    def testStatementsWithWhitespace(self):
        self.assertTokenization("   sin   ( 45 )   ", ['sin', '(', '45', ')'])

    def assertTokenizationFails(self, statement):
        def tokenize():
            tokenizer = Tokenizer(statement)
            for token in tokenizer:
                pass

        self.assertRaises(TokenizerError, tokenize)

        # self.assertEqual(len(input_str), tokenizer.cursor, f'cannot tokenize whole input, leftover: {tokenizer.input_left_over()}')

    def testInvalidOperators1(self):
        self.assertTokenizationFails("2 + $")

    def testInvalidOperators2(self):
        self.assertTokenizationFails("2 & 3")

    def testUnknownSymbol(self):
        self.assertTokenizationFails("2 # 3")

    def testInvalidNumberFormat(self):
        self.assertTokenizationFails("1.2.3 + 4")


if __name__ == "__main__":
    unittest.main()