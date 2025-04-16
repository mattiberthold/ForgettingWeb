from itertools import chain, combinations
from typing import Set

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation, HTModel
from ForgettingWeb.semantic_modules.ht_model_column import HTModelColumn
from ForgettingWeb.semantic_modules.operator_powerset import OperatorPowerset


class Models2LP:
    @staticmethod
    def apply(models: Set[HTModelColumn], signature: Set[Literal]) -> LogicProgram:
        ps = OperatorPowerset.apply(signature)
        lp = LogicProgram()
        # create rules contradicting missing total models
        for s in ps:
            boolean = False
            for c in models:
                if c.y.__eq__(s):
                    boolean = True
            if not boolean:
                lp.add(Models2LP.contradict_total(s, signature))

        # create rules contradicting the witnesses
        for c in models:
            counter_models = c.get_counter_models()
            for counter_model in counter_models:
                lp.add(Models2LP.contradict_witness(counter_model, signature))
        return lp

    @staticmethod
    def contradict_total(total: ClassicalInterpretation, signature: Set[Literal]):
        return Rule(set(), set(), signature.difference(total), total)

    @staticmethod
    def contradict_witness(witness: HTModel, signature: Set[Literal]):
        return Rule(signature.difference(witness.x), witness.x,
                    signature.difference(witness.y), witness.y.difference(witness.x))
