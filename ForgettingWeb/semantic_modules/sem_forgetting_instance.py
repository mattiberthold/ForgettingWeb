from typing import List, Set

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation
from forgetting_operators_logic_programming.semantic_modules.ht_model_column import HTModelColumn
from forgetting_operators_logic_programming.semantic_modules.operator_powerset import OperatorPowerset


class SemForgettingInstance:
    def __init__(self, sem_prog: Set[HTModelColumn], y_wo_v_literals: ClassicalInterpretation,
                 v_literals: ClassicalInterpretation):
        self.omega = dict()
        self.sorted_columns = dict()
        self.y_wo_v_literals = y_wo_v_literals
        self.v_literals = v_literals
        for y in OperatorPowerset.apply(y_wo_v_literals):
            self.sorted_columns[y] = set()
            for c in sem_prog:
                if c.y.difference(v_literals) == y:
                    if c.is_relevant(v_literals):
                        self.sorted_columns[y].add(c)

    def determine_omega(self):
        for y in OperatorPowerset.apply(self.y_wo_v_literals):
            if len(self.sorted_columns[y]) == 0:
                self.omega[y] = False
                continue
            is_least_c = dict()
            for c in self.sorted_columns[y]:
                is_least_c[c] = True
            for x in OperatorPowerset.apply(y):
                exists_anti_witness = False
                for c in self.sorted_columns[y]:
                    if c.get_block_len(x, self.v_literals) == 0:
                        exists_anti_witness = True
                        break
                if not exists_anti_witness:
                    continue
                for c in self.sorted_columns[y]:
                    if c.get_block_len(x, self.v_literals) > 0:
                        is_least_c[c] = False
            self.omega[y] = True
            for c in self.sorted_columns[y]:
                if is_least_c[c]:
                    self.omega[y] = False
                    break

