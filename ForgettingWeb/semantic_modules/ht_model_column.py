from itertools import chain, combinations
from typing import Set

from forgetting_operators_logic_programming.semantic_modules.operator_powerset import OperatorPowerset
from forgetting_operators_logic_programming.semantic_modules.ht_model import HTModel
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation


def create_ht_models(y: ClassicalInterpretation):
    ps = OperatorPowerset.apply(y)
    out = set()
    for x in ps:
        out.add(HTModel(ClassicalInterpretation(set(x)), ClassicalInterpretation(set(y))))
    return out


class HTModelColumn:
    def __init__(self, y: ClassicalInterpretation):
        self.y = ClassicalInterpretation(y)
        self.ht_models = create_ht_models(y)

    def __str__(self):
        str_ = ''
        for model in self.ht_models:
            str_ += str(model) + ' '
        return str_

    def get_block_len(self, x_wo_v: ClassicalInterpretation, v: ClassicalInterpretation):
        models = self.ht_models.copy()
        iter_ = 0
        for m in models:
            if m.x.difference(v) == x_wo_v:
                iter_ += 1
        return iter_

    def is_relevant(self, v: ClassicalInterpretation):
        y_wo_v = ClassicalInterpretation(self.y.copy().difference(v))
        return self.get_block_len(y_wo_v, v) == 1

    def rm_model(self, x: ClassicalInterpretation):
        for model in self.ht_models:
            if model.x.__eq__(x) and not model.x.__eq__(self.y):
                self.ht_models.remove(model)
                break

    def clear(self):
        self.ht_models = set()
        self.ht_models.add(HTModel(self.y, self.y))

    def add_model(self, x: ClassicalInterpretation):
        if self.y.__eq__(x):
            return
        is_new = True
        for model in self.ht_models:
            if model.x.__eq__(x) and not model.x.__eq__(self.y):
                is_new = False
        if is_new:
            self.ht_models.add(HTModel(x, self.y))

    def get_reduced_column(self, v: ClassicalInterpretation):
        y_wo_v = ClassicalInterpretation(self.y.copy().difference(v))
        new_column = HTModelColumn(y_wo_v)
        new_column.ht_models.clear()
        ps = OperatorPowerset.apply(y_wo_v)
        for i in ps:
            if self.get_block_len(i, v) != 0:
                new_column.ht_models.add(HTModel(i, y_wo_v))
        return new_column

    def get_xs(self):
        xs = []
        for model in self.ht_models:
            xs.append(model.x)
        return xs

    def get_counter_models(self) -> Set[HTModel]:
        ps = OperatorPowerset.apply(self.y)
        xs = self.get_xs()
        counter_models = set()
        for s in ps:
            if s not in xs:
                counter_models.add(HTModel(s, self.y))
        return counter_models

