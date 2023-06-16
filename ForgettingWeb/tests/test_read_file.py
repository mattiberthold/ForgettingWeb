import unittest

from forgetting_operators_logic_programming.classes.rule import Rule
from forgetting_operators_logic_programming.import_export.read_demo_file import read_demo_file


class TestReadFile(unittest.TestCase):
    def test_read_file(self):
        program, variables_to_be_forgotten = read_demo_file()
        self.assertEqual(len(program.rules), 3)
        self.assertTrue(variables_to_be_forgotten.pop().literal_str == 'q')
        self.assertIn(Rule.from_str('a :-    q'), program.rules)
        self.assertIn(Rule.from_str('b :- ~q'), program.rules)
        self.assertIn(Rule.from_str('q:-c'), program.rules)
        self.assertNotIn(Rule.from_str('b :- q'), program.rules)

    def test_read_file_not(self):
        program, variables_to_be_forgotten = read_demo_file()
        self.assertEqual(len(program.rules), 3)
        self.assertTrue(variables_to_be_forgotten.pop().literal_str == 'q')
        self.assertIn(Rule.from_str('a :-    q'), program.rules)
        self.assertIn(Rule.from_str('b :- not q'), program.rules)
        self.assertIn(Rule.from_str('q:-c'), program.rules)
        self.assertNotIn(Rule.from_str('b :- q'), program.rules)

    def test_read_file_with_not_in_file(self):
        program, variables_to_be_forgotten = read_demo_file('demo_file_with_not.txt')
        self.assertEqual(len(program.rules), 3)
        self.assertTrue(variables_to_be_forgotten.pop().literal_str == 'q')
        self.assertIn(Rule.from_str('a :-    q'), program.rules)
        self.assertIn(Rule.from_str('b :- not   q'), program.rules)
        self.assertIn(Rule.from_str('q:-c'), program.rules)
        self.assertNotIn(Rule.from_str('b :- q'), program.rules)
