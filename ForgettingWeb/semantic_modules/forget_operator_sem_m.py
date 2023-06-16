from typing import Set

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from forgetting_operators_logic_programming.semantic_modules.ht_model_column import HTModelColumn
from forgetting_operators_logic_programming.semantic_modules.operator_powerset import OperatorPowerset
from forgetting_operators_logic_programming.semantic_modules.sem_forgetting_instance import SemForgettingInstance


class ForgetOperatorSemM:
    @staticmethod
    def apply(instance: SemForgettingInstance) -> Set[HTModelColumn]:
        instance.determine_omega()
        out = set()
        for y in instance.sorted_columns:
            if instance.omega[y]:
                out = out.union(ForgetOperatorSemM.column_r(instance, y))
            else:
                out = out.union(ForgetOperatorSemM.column_sp(instance, y))
        return out

    @staticmethod
    def column_r(instance: SemForgettingInstance, y: frozenset) -> Set[HTModelColumn]:
        if len(instance.sorted_columns[y]) == 0:
            return set()
        c = HTModelColumn(ClassicalInterpretation(set(y)))
        c.clear()
        for c_old in instance.sorted_columns[y]:
            if c_old.is_relevant(instance.v_literals):
                for x in OperatorPowerset.apply(y):
                    if c_old.get_block_len(x, instance.v_literals) > 0:
                        c.add_model(ClassicalInterpretation(x))
        return {c}

    @staticmethod
    def column_sp(instance: SemForgettingInstance, y: frozenset) -> Set[HTModelColumn]:
        if len(instance.sorted_columns[y]) == 0:
            return set()
        c = HTModelColumn(ClassicalInterpretation(set(y)))
        for c_old in instance.sorted_columns[y]:
            for x in OperatorPowerset.apply(y):
                if c_old.get_block_len(x, instance.v_literals) == 0:
                    c.rm_model(ClassicalInterpretation(x))
        return {c}
