import unittest

from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset
from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.import_export.read_demo_file import read_demo_file
from ForgettingWeb.semantic_modules.forget_operator_sem_m import ForgetOperatorSemM
from ForgettingWeb.semantic_modules.forget_operator_sem_r import ForgetOperatorSemR
from ForgettingWeb.semantic_modules.forget_operator_sem_sp import ForgetOperatorSemSP
from ForgettingWeb.semantic_modules.forget_operator_sem_up import ForgetOperatorSemUP
from ForgettingWeb.forgetting_modules.forget_operator_rR import ForgetOperatorRR
from ForgettingWeb.forgetting_modules.forget_operator_rSP import ForgetOperatorRSP
from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.lp_to_models import LP2Models
from ForgettingWeb.semantic_modules.models_to_lp import Models2LP
from ForgettingWeb.semantic_modules.sem_rel_forget_instance import SemRelForgetInstance
from ForgettingWeb.forgetting_modules.forget_operator_u import ForgetOperatorUniform

from ForgettingWeb.forgetting_modules.forget_operator_semantic_wrapper import ForgetOperatorSemrR
from ForgettingWeb.forgetting_modules.forget_operator_semantic_wrapper import ForgetOperatorSemrSP


class TestRelSemantics(unittest.TestCase):
    def test_determine_omega(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        d = Literal('d')

        abcdq = ClassicalInterpretation({a, b, d, c, q})
        abcd = ClassicalInterpretation({a, b, d, c})
        abdq = ClassicalInterpretation({a, b, d, q})
        abd = ClassicalInterpretation({a, b, d})
        acdq = ClassicalInterpretation({a, c, d, q})
        acd = ClassicalInterpretation({a, d, c})
        adq = ClassicalInterpretation({a, d, q})
        ad = ClassicalInterpretation({a, d})
        bcdq = ClassicalInterpretation({b, d, c, q})
        bcd = ClassicalInterpretation({b, d, c})
        bdq = ClassicalInterpretation({b, d, q})
        bd = ClassicalInterpretation({b, d})
        cdq = ClassicalInterpretation({d, c, q})
        cd = ClassicalInterpretation({d, c})
        dq = ClassicalInterpretation({q})
        d = ClassicalInterpretation({d})
        abcq = ClassicalInterpretation({a, b, c, q})
        abc = ClassicalInterpretation({a, b, c})
        abq = ClassicalInterpretation({a, b, q})
        ab = ClassicalInterpretation({a, b})
        acq = ClassicalInterpretation({a, c, q})
        ac = ClassicalInterpretation({a, c})
        aq = ClassicalInterpretation({a, q})
        a = ClassicalInterpretation({a})
        bcq = ClassicalInterpretation({b, c, q})
        bc = ClassicalInterpretation({b, c})
        bq = ClassicalInterpretation({b, q})
        b = ClassicalInterpretation({b})
        cq = ClassicalInterpretation({c, q})
        c = ClassicalInterpretation({c})
        q = ClassicalInterpretation({q})
        empty = ClassicalInterpretation(set())

        col_acq = HTModelColumn(acq)
        col_ac = HTModelColumn(ac)
        col_acq.clear()
        col_acq.add_model(ac)
        col_acq.add_model(empty)
        col_ac.clear()
        col_ac.add_model(a)

        col_abcdq = HTModelColumn(abcdq)
        col_abcd = HTModelColumn(abcd)
        col_abcdq.clear()
        col_abcdq.add_model(abcq)
        col_abcdq.add_model(empty)
        col_abcd.clear()
        col_abcd.add_model(a)

        col_abdq = HTModelColumn(abdq)
        col_abd = HTModelColumn(abd)
        col_abdq.clear()
        col_abdq.add_model(empty)
        col_abd.clear()
        col_abd.add_model(a)

        y_wo_v_literals = ClassicalInterpretation({a, b, c, d})
        v_literals = ClassicalInterpretation({q})
        b_literals = ClassicalInterpretation({a, b, c})

        cols = {col_acq, col_ac, col_abcdq, col_abcd, col_abdq, col_abd}

        rel_forget_instance = SemRelForgetInstance(cols, y_wo_v_literals, v_literals, b_literals)

        rel_forget_instance.determine_omega()

        # for y in rel_forget_instance.sorted_columns.keys():
        #     print(len(rel_forget_instance.sorted_columns[y]))
        #     for s in rel_forget_instance.sorted_columns[y]:
        #         print(s)

        self.assertFalse(rel_forget_instance.omega[frozenset({a, c})])
        self.assertFalse(rel_forget_instance.omega[frozenset({a, b, c, d})])
        self.assertTrue(rel_forget_instance.omega[frozenset({a, b, d})])

    def test_frR(self):
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        d = Literal('d')
        e = Literal('e')
        f = Literal('f')

        rule1 = Rule({a}, {b, c}, set(), set())
        rule2 = Rule({c}, {d}, set(), set())
        rule3 = Rule({b}, set(), set(), set())

        prog1 = LogicProgram({rule1, rule2, rule3})

        v_lit1 = [b, c]
        b_lit1 = [a, b, d]
        synresult1 = ForgetOperatorRR.apply(prog1, v_lit1, b_lit1)
        semresult1 = ForgetOperatorSemrR.apply(SemRelForgetInstance(LP2Models.apply(prog1),
                                                                    ClassicalInterpretation(
                                                                        prog1.get_signature().difference(v_lit1)),
                                                                    ClassicalInterpretation(v_lit1),
                                                                    ClassicalInterpretation(b_lit1)))
        synresult1 = Models2LP.apply(LP2Models.apply(synresult1), set(b_lit1))
        semresult1 = Models2LP.apply(semresult1, set(b_lit1))
        self.assertEqual(synresult1, semresult1)

        synresult1 = ForgetOperatorRSP.apply(prog1, v_lit1, b_lit1)
        semresult1 = ForgetOperatorSemrSP.apply(SemRelForgetInstance(LP2Models.apply(prog1),
                                                                     ClassicalInterpretation(
                                                                         prog1.get_signature().difference(v_lit1)),
                                                                     ClassicalInterpretation(v_lit1),
                                                                     ClassicalInterpretation(b_lit1)))
        synresult1 = Models2LP.apply(LP2Models.apply(synresult1), set(b_lit1))
        semresult1 = Models2LP.apply(semresult1, set(b_lit1))
        self.assertEqual(synresult1, semresult1)

        rule4 = Rule({a}, set(), {b}, set())
        rule5 = Rule({b}, set(), {a}, set())
        rule6 = Rule({c}, set(), set(), set())

        prog2 = LogicProgram({rule4, rule5, rule6})

        v_lit2 = [b, c]
        b_lit2 = [a, c]
        synresult2 = ForgetOperatorRR.apply(prog2, v_lit2, b_lit2)
        semresult2 = ForgetOperatorSemrR.apply(SemRelForgetInstance(LP2Models.apply(prog2),
                                                                    ClassicalInterpretation(
                                                                        prog2.get_signature().difference(v_lit2)),
                                                                    ClassicalInterpretation(v_lit2),
                                                                    ClassicalInterpretation(b_lit2)))
        synresult2 = Models2LP.apply(LP2Models.apply(synresult2), set(b_lit2))
        semresult2 = Models2LP.apply(semresult2, set(b_lit2))
        self.assertEqual(synresult2, semresult2)

        synresult2 = ForgetOperatorRSP.apply(prog2, v_lit2, b_lit2)
        semresult2 = ForgetOperatorSemrSP.apply(SemRelForgetInstance(LP2Models.apply(prog2),
                                                                     ClassicalInterpretation(
                                                                         prog2.get_signature().difference(v_lit2)),
                                                                     ClassicalInterpretation(v_lit2),
                                                                     ClassicalInterpretation(b_lit2)))
        synresult2 = Models2LP.apply(LP2Models.apply(synresult2), set(b_lit2))
        semresult2 = Models2LP.apply(semresult2, set(b_lit2))
        self.assertEqual(synresult2, semresult2)

        # print(ForgetOperatorRR.apply(prog1, v_lit1, b_lit1))
        # print()
        # print(ForgetOperatorRSP.apply(prog1, v_lit1, b_lit1))
        # print()
        # print(ForgetOperatorRR.apply(prog2, v_lit2, b_lit2))
        # print()
        # print(ForgetOperatorRSP.apply(prog2, v_lit2, b_lit2))

    def test_rsp_op(self):
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        d = Literal('d')
        q = Literal('q')

        rule1 = Rule({a}, {b, q}, set(), set())
        rule2 = Rule({c}, {d, q}, set(), set())
        rule3 = Rule({q}, set(), set(), {q})

        prog1 = LogicProgram({rule1, rule2, rule3})
        q_literals = [q]
        b_literals = [a, b, c, d]

        result = ForgetOperatorRSP.apply(prog1, q_literals, b_literals)

        print(result)
