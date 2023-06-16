from typing import Set

from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from forgetting_operators_logic_programming.semantic_modules.ht_model_column import HTModelColumn
from forgetting_operators_logic_programming.semantic_modules.operator_powerset import OperatorPowerset
from forgetting_operators_logic_programming.semantic_modules.sem_forgetting_instance import SemForgettingInstance


class ForgetOperatorSemUP:
    @staticmethod
    def apply(instance: SemForgettingInstance) -> Set[HTModelColumn]:
        out = set()
        for y in instance.sorted_columns:
            if len(instance.sorted_columns[y]) == 0:
                continue
            c_new = HTModelColumn(y)
            first = True
            for c in instance.sorted_columns[y]:
                if first:
                    first = False
                    c_new = c.get_reduced_column(instance.v_literals)
                else:
                    c = c.get_reduced_column(instance.v_literals)
                    c_new = ForgetOperatorSemUP.intersect_each_model_of_two_columns(c_new, c)
            out.add(c_new)
        return out

    @staticmethod
    def intersect_each_model_of_two_columns(c1: HTModelColumn, c2: HTModelColumn):
        c_new = HTModelColumn(c1.y)
        c_new.clear()
        for m1 in c1.ht_models:
            if m1.x == m1.y:
                continue
            for m2 in c2.ht_models:
                if m2.x == m2.y:
                    continue
                c_new.add_model(ClassicalInterpretation(m1.x.intersection(m2.x)))
        return c_new
