import unittest

from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.forgetting_modules.operator_normalize import NormalizeOperator
from ForgettingWeb.import_export.read_demo_file import read_demo_file


class TestNormaliseOperator(unittest.TestCase):
    def test_normalize_operator(self):
        program, _ = read_demo_file('not_normal.txt')
        normalised_program = NormalizeOperator.apply(program)
        self.assertEqual(len(normalised_program.rules), 1)
        normalised_rule = Rule.from_str('a :- e, b, c, ~d')
        self.assertTrue(normalised_program.contains_rule(normalised_rule))
