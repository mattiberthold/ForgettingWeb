from itertools import combinations, chain
from typing import Set

from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation
from forgetting_operators_logic_programming.semantic_modules.ht_model_column import HTModelColumn


def powerset(iterable):
    s = list(iterable)
    list_of_tuples = set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    out = set({})
    for el in list_of_tuples:
        out.add(frozenset(list(el)))
    return out


class LP2Models:
    @staticmethod
    def apply(logic_program: LogicProgram) -> Set[HTModelColumn]:
        signature = logic_program.get_signature()
        columns = set()
        ps = powerset(signature)
        for y in ps:
            boolean = True
            if not ClassicalInterpretation(y).satisfies_lp(logic_program):
                boolean = False
            if boolean:
                columns.add(HTModelColumn(y))
        for c in columns:
            rm = set()
            for model in c.ht_models:
                if not model.satisfies_lp(logic_program):
                    rm.add(model)
            c.ht_models.difference_update(rm)
        return columns
