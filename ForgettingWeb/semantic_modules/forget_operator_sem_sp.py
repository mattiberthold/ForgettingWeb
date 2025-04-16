from typing import Set

from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset
from ForgettingWeb.semantic_modules.sem_forgetting_instance import SemForgettingInstance


class ForgetOperatorSemSP:
    @staticmethod
    def apply(instance: SemForgettingInstance) -> Set[HTModelColumn]:
        out = set()
        for y in instance.sorted_columns:
            if len(instance.sorted_columns[y]) == 0:
                continue
            c = HTModelColumn(y)
            for c_old in instance.sorted_columns[y]:
                for x in OperatorPowerset.apply(y):
                    if c_old.get_block_len(x, instance.v_literals) == 0:
                        c.rm_model(ClassicalInterpretation(x))
            out.add(c)
        return out
