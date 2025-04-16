from typing import Set

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule


class ClassicalInterpretation(Set[Literal]):
    def __str__(self):
        str_ = ''
        for e in self:
            str_ += str(e)
        return str_

    def __hash__(self):
        h = 0
        for el in self:
            h += hash(el)
        return h

    def satisfies(self, r: Rule) -> bool:
        # Y classical model?
        if not self.intersection(r.body_negative_negative.union(r.body_positive)). \
                __eq__(r.body_negative_negative.union(r.body_positive)):
            return True
        if len(self.intersection(r.body_negative.union(r.head))) != 0:
            return True
        return False

    def satisfies_lp(self, lp: LogicProgram) -> bool:
        for r in lp:
            if not self.satisfies(r):
                return False
        return True


class HTModel:
    def __init__(self, x: ClassicalInterpretation, y: ClassicalInterpretation):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.y) + hash(self.x)

    def satisfies(self, r: Rule) -> bool:
        # Y classical model?
        if not self.y.intersection(r.body_negative_negative.union(r.body_positive)). \
                __eq__(r.body_negative_negative.union(r.body_positive)):
            return True
        if len(self.y.intersection(r.body_negative)) != 0:
            return True
        # X model of P^Y?
        if not self.x.intersection(r.body_positive).__eq__(r.body_positive):
            return True
        if len(self.x.intersection(r.head)) != 0:
            return True
        return False

    def satisfies_lp(self, lp: LogicProgram) -> bool:
        for r in lp:
            if not self.satisfies(r):
                return False
        return True

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'
