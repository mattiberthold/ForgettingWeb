import unittest

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.import_export.read_demo_file import read_demo_file
from ForgettingWeb.semantic_modules.forget_operator_sem_m import ForgetOperatorSemM
from ForgettingWeb.semantic_modules.forget_operator_sem_r import ForgetOperatorSemR
from ForgettingWeb.semantic_modules.forget_operator_sem_sp import ForgetOperatorSemSP
from ForgettingWeb.semantic_modules.forget_operator_sem_up import ForgetOperatorSemUP
from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.lp_to_models import LP2Models
from ForgettingWeb.semantic_modules.models_to_lp import Models2LP
from ForgettingWeb.semantic_modules.sem_forgetting_instance import SemForgettingInstance
from ForgettingWeb.forgetting_modules.forget_operator_u import ForgetOperatorUniform

class TestSemantics(unittest.TestCase):
    def test_column(self):
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        y = ClassicalInterpretation({a, b, c})
        column = HTModelColumn(y)
        self.assertEqual(column.y, y)
        self.assertEqual(len(column.ht_models), 8)
        column.rm_model(ClassicalInterpretation({a, c}))
        self.assertEqual(len(column.ht_models), 7)
        self.assertTrue(column.is_relevant(ClassicalInterpretation({b})))
        self.assertTrue(column.is_relevant(ClassicalInterpretation({})))

        self.assertFalse(column.is_relevant(ClassicalInterpretation({a})))
        self.assertFalse(column.is_relevant(ClassicalInterpretation({c})))
        self.assertFalse(column.is_relevant(ClassicalInterpretation({a, b})))
        self.assertFalse(column.is_relevant(ClassicalInterpretation({a, c})))
        self.assertFalse(column.is_relevant(ClassicalInterpretation({b, c})))
        self.assertFalse(column.is_relevant(ClassicalInterpretation({a, b, c})))

        reduced_column = column.get_reduced_column(ClassicalInterpretation({b}))
        self.assertEqual(len(reduced_column.ht_models), 4)

    def test_lp2models(self):
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        r1 = Rule({a}, set(), set(), {a})
        r2 = Rule({b}, {a}, set(), set())
        r3 = Rule({c}, set(), {a}, set())
        lp = LogicProgram({r1, r2, r3})

        i = HTModel({b}, {a, b, c})

        self.assertFalse(i.satisfies(r1))
        self.assertTrue(i.satisfies(r3))

        columns = LP2Models.apply(lp)
        self.assertEqual(len(columns), 4)
        model_count = 0
        for c in columns:
            model_count += len(c.ht_models)
        self.assertEqual(model_count, 6)

        # print('program:')
        # print(lp)
        # print('models:')
        # for c in models:
        #     print(c.y)
        #     print(c)

    def test_model2lp(self):
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        r1 = Rule({a}, set(), set(), {a})
        r2 = Rule({b}, {a}, set(), set())
        r3 = Rule({c}, set(), {a}, set())
        lp = LogicProgram({r1, r2, r3})

        lp_new = Models2LP.apply(LP2Models.apply(lp), {a, b, c})
        self.assertEqual(len(lp_new), 16)
        lp_new = Models2LP.apply(LP2Models.apply(lp_new), {a, b, c})
        self.assertEqual(len(lp_new), 16)

    def test_sem_forgetting_instance(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        r1 = Rule({q}, set(), set(), {q})
        r2 = Rule({a}, {q}, set(), set())
        r3 = Rule({b}, set(), {q}, set())
        lp = LogicProgram({r1, r2, r3})
        sem_lp = LP2Models.apply(lp)
        sem_forgetting_instance = SemForgettingInstance(sem_lp, ClassicalInterpretation({a, b}),
                                                        ClassicalInterpretation({q}))

        self.assertEqual(sem_forgetting_instance.sorted_columns.__len__(), 4)

    def test_determine_omega(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        r1 = Rule({q}, set(), set(), {q})
        r2 = Rule({a}, {q}, set(), set())
        r3 = Rule({b}, set(), {q}, set())
        lp = LogicProgram({r1, r2, r3})
        sem_lp = LP2Models.apply(lp)
        sem_forgetting_instance = SemForgettingInstance(sem_lp, ClassicalInterpretation({a, b}),
                                                        ClassicalInterpretation({q}))
        sem_forgetting_instance.determine_omega()

        self.assertTrue(sem_forgetting_instance.omega[frozenset({a, b})])
        self.assertFalse(sem_forgetting_instance.omega[frozenset({b})])
        self.assertFalse(sem_forgetting_instance.omega[frozenset({a})])
        self.assertFalse(sem_forgetting_instance.omega[frozenset({})])

    def test_sem_forgetting(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        r1 = Rule({q}, set(), set(), {q})
        r2 = Rule({a}, {q}, set(), set())
        r3 = Rule({b}, set(), {q}, set())
        lp = LogicProgram({r1, r2, r3})
        sem_lp = LP2Models.apply(lp)
        # for c in sem_lp:
        #     print(c)
        sem_forgetting_instance = SemForgettingInstance(sem_lp, ClassicalInterpretation({a, b}),
                                                        ClassicalInterpretation({q}))

        sem_lp_new = ForgetOperatorSemSP.apply(sem_forgetting_instance)
        # for c in sem_lp_new:
        #     print(c)
        # print(Models2LP.apply(sem_lp_new, {a, b}))
        self.assertEqual(len(sem_lp_new), 3)
        self.assertEqual(len(Models2LP.apply(sem_lp_new, {a, b})), 6)

        sem_lp_new = ForgetOperatorSemR.apply(sem_forgetting_instance)
        # for c in sem_lp_new:
        #     print(c)
        # print(Models2LP.apply(sem_lp_new, {a, b}))
        self.assertEqual(len(sem_lp_new), 3)
        self.assertEqual(len(Models2LP.apply(sem_lp_new, {a, b})), 4)

        sem_lp_new = ForgetOperatorSemM.apply(sem_forgetting_instance)
        # for c in sem_lp_new:
        #     print(c)
        # print(Models2LP.apply(sem_lp_new, {a, b}))
        self.assertEqual(len(sem_lp_new), 3)
        self.assertEqual(len(Models2LP.apply(sem_lp_new, {a, b})), 4)

        column_abq = HTModelColumn(ClassicalInterpretation({a, b, q}))
        column_abq.rm_model(ClassicalInterpretation({a, b}))
        column_abq.rm_model(ClassicalInterpretation({a}))
        column_abq.rm_model(ClassicalInterpretation({b, q}))
        column_abq.rm_model(ClassicalInterpretation({b}))
        column_abq.rm_model(ClassicalInterpretation({q}))
        column_abq.rm_model(ClassicalInterpretation({}))

        column_ab = HTModelColumn(ClassicalInterpretation({a, b}))
        column_ab.rm_model(ClassicalInterpretation({a}))
        column_ab.rm_model(ClassicalInterpretation({}))

        column_aq = HTModelColumn(ClassicalInterpretation({a, q}))

        column_a = HTModelColumn(ClassicalInterpretation({a}))
        column_a.rm_model(ClassicalInterpretation({}))

        sem_lp_2 = {column_abq, column_ab, column_aq, column_a}

        sem_forgetting_instance_2 = SemForgettingInstance(sem_lp_2, ClassicalInterpretation({a, b}),
                                                          ClassicalInterpretation({q}))

        sem_lp_new_2 = ForgetOperatorSemM.apply(sem_forgetting_instance_2)
        # for c in sem_lp_new_2:
        #     print(c)
        # print(Models2LP.apply(sem_lp_new_2, {a, b}))
        self.assertEqual(len(sem_lp_new_2), 2)
        self.assertEqual(len(Models2LP.apply(sem_lp_new_2, {a, b})), 4)

    def test_sem_up(self):
        q = Literal('q')
        a = Literal('a')
        b = Literal('b')
        abq = ClassicalInterpretation({a, b, q})
        ab = ClassicalInterpretation({a, b})
        aq = ClassicalInterpretation({a, q})
        a = ClassicalInterpretation({a})
        bq = ClassicalInterpretation({b, q})
        b = ClassicalInterpretation({b})
        q = ClassicalInterpretation({q})
        e = ClassicalInterpretation({})

        c1 = HTModelColumn(ab)

        c1.rm_model(a)
        c1.rm_model(e)

        c2 = HTModelColumn(ab)
        c2.rm_model(b)
        c2.rm_model(e)

        c3 = HTModelColumn(ab)
        c3.rm_model(b)

        c_12 = ForgetOperatorSemUP.intersect_each_model_of_two_columns(c1, c2)
        self.assertEqual(len(c_12.ht_models), 2)
        c_13 = ForgetOperatorSemUP.intersect_each_model_of_two_columns(c1, c3)
        self.assertEqual(len(c_13.ht_models), 2)
        c_22 = ForgetOperatorSemUP.intersect_each_model_of_two_columns(c2, c2)
        self.assertEqual(len(c_22.ht_models), 2)
        c_33 = ForgetOperatorSemUP.intersect_each_model_of_two_columns(c3, c3)
        self.assertEqual(len(c_33.ht_models), 3)

    def test_f_u(self):
        program, variables_to_be_forgotten = read_demo_file()

        new_program = ForgetOperatorUniform.apply(program, variables_to_be_forgotten)

        self.assertEqual(len(new_program), 2)

        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        r1 = Rule({a}, set(), set(), {a})
        r2 = Rule({b}, set(), set(), set())
        r3 = Rule({c}, set(), set(), set())
        program = LogicProgram({r1, r2, r3})
        new_program = ForgetOperatorUniform.apply(program, [a])

        self.assertEqual(len(new_program), 6)

