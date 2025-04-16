from typing import Set

from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset
from ForgettingWeb.semantic_modules.sem_forgetting_instance import SemForgettingInstance
from ForgettingWeb.semantic_modules.sem_rel_forget_instance import SemRelForgetInstance


class ForgetOperatorSemrR:
    @staticmethod
    def apply(instance: SemRelForgetInstance) -> Set[HTModelColumn]:
        out = set()
        for y in instance.sorted_columns:
            if len(instance.sorted_columns[y]) == 0:
                continue
            c = HTModelColumn(y)
            c.clear()
            for c_old in instance.sorted_columns[y]:
                if c_old.is_relevant(instance.v_literals):
                    for x in OperatorPowerset.apply(y):
                        if c_old.get_block_len(x, instance.v_literals) > 0:
                            c.add_model(ClassicalInterpretation(x))
            out.add(c)
        return out
