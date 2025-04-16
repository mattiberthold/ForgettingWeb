from typing import Set

from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset
from ForgettingWeb.semantic_modules.sem_forgetting_instance import SemForgettingInstance


class SemRelForgetInstance(SemForgettingInstance):
    def __init__(self, sem_prog: Set[HTModelColumn], y_wo_v_literals: ClassicalInterpretation,
                 v_literals: ClassicalInterpretation, b_literals: ClassicalInterpretation):
        SemForgettingInstance.__init__(self, sem_prog, y_wo_v_literals, v_literals)
        self.rel_omega = dict()
        self.b_literals = y_wo_v_literals.difference(b_literals)
        self.contr_b_literals = y_wo_v_literals.difference(b_literals)

        # remove additional columns
        for y in OperatorPowerset.apply(self.y_wo_v_literals.union(self.contr_b_literals)):
            y_wo_b = ClassicalInterpretation(y.copy().difference(self.contr_b_literals))
            rm = set()
            for col in self.sorted_columns[y]:
                if col.get_block_len(y_wo_b, self.contr_b_literals.union(self.v_literals)) != 1:
                    rm.add(col)
            self.sorted_columns[y] = self.sorted_columns[y].difference(rm)