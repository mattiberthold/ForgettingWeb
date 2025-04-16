import unittest

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.forgetting_modules.forget_operator_forget3 import ForgetOperatorForget3


class TestEW(unittest.TestCase):
    def test_forget3(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        r1 = Rule({q}, set(), set(), {q})
        r2 = Rule({a}, {q}, set(), set())
        r3 = Rule({b}, set(), {q}, set())
        lp = LogicProgram({r1, r2, r3})

        lp_new = ForgetOperatorForget3.apply(lp, [])

        self.assertEqual(lp, lp_new)

        lp_new = ForgetOperatorForget3.apply(lp, [q])

        print(lp_new)
