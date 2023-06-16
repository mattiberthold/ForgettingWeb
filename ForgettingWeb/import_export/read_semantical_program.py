import re
from typing import List

from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.classes.rule import Rule
from forgetting_operators_logic_programming.semantic_modules.ht_model import HTModel, ClassicalInterpretation
from forgetting_operators_logic_programming.semantic_modules.ht_model_column import HTModelColumn
from forgetting_operators_logic_programming.semantic_modules.sem_forgetting_instance import SemForgettingInstance


def read_input_models(input_model_str: str):
    model_strings = re.split('[<\n]+', input_model_str.strip().replace(' ', '').replace('>', ''))
    models = set()
    for m in model_strings:
        if not m.__eq__(''):
            x, y = m.split(',')
            models.add(HTModel(ClassicalInterpretation(list(x)),
                               ClassicalInterpretation(list(y))))

    signature = set()
    columns = dict()
    classical_models = set()

    for m in models:
        if m.y in classical_models:
            columns[m.y].add_model(m.x)
        else:
            columns[m.y] = HTModelColumn(m.y)
            columns[m.y].clear()
            columns[m.y].add_model(m.x)
            classical_models.add(m.y)
            signature = signature.union(m.y)

    return set(columns.values()), signature
