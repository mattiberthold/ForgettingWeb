from typing import Set

from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset


class SemForgettingInstance:
    def __init__(self, sem_prog: Set[HTModelColumn], y_wo_v_literals: ClassicalInterpretation,
                 v_literals: ClassicalInterpretation):
        self.omega = dict()
        self.sorted_columns = dict()
        self.y_wo_v_literals = y_wo_v_literals
        self.v_literals = v_literals
        for y in OperatorPowerset.apply(y_wo_v_literals):
            self.sorted_columns[y] = set()
            for col in sem_prog:
                if col.y.difference(v_literals) == y:
                    if col.is_relevant(v_literals):
                        self.sorted_columns[y].add(col)

    def determine_omega(self):
        for y in OperatorPowerset.apply(self.y_wo_v_literals):
            if len(self.sorted_columns[y]) == 0:
                self.omega[y] = False
                continue
            is_least_col = dict()
            for col in self.sorted_columns[y]:
                is_least_col[col] = True
            for x in OperatorPowerset.apply(y):
                exists_anti_witness = False
                for col in self.sorted_columns[y]:
                    if col.get_block_len(x, self.v_literals) == 0:
                        exists_anti_witness = True
                        break
                if not exists_anti_witness:
                    continue
                for col in self.sorted_columns[y]:
                    if col.get_block_len(x, self.v_literals) > 0:
                        is_least_col[col] = False
            self.omega[y] = True
            for col in self.sorted_columns[y]:
                if is_least_col[col]:
                    self.omega[y] = False
                    break

