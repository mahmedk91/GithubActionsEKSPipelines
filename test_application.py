import unittest
from unittest.mock import patch
from io import StringIO
from application import printOnConsole


class UnitTests(unittest.TestCase):

    # This is a stupid unit test. It mocks the print function and asserts the output
    # Since, there is no logic in our application, there is nothing to test :P
    # I just created it to have at least one unit test to make part of the CI/CD pipeline
    @patch('sys.stdout', new_callable=StringIO)
    def test_printOnConsole(self, mock_stdout):
        printOnConsole()
        self.assertEqual(mock_stdout.getvalue(), "Hello World\n")

if __name__ == '__main__':
    unittest.main()
