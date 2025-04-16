from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule


class OperatorSemiShift:

    @staticmethod
    def apply(input_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        for q_literal in q_literals:
            input_program = OperatorSemiShift.apply_(input_program, q_literal)

        return input_program

    @staticmethod
    def apply_(input_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        partition = input_program.get_occurrence_partition(q_literal)
        new_rules = set()

        for rule in partition.r4 | partition.r3:
            new_rules.add(Rule(rule.head.difference({q_literal}),
                               rule.body_positive,
                               rule.body_negative.union({q_literal}),
                               rule.body_negative_negative))
            new_rules.add(Rule({q_literal},
                               rule.body_positive,
                               rule.body_negative | rule.head.difference({q_literal}),
                               rule.body_negative_negative))

        return LogicProgram(set(new_rules | partition.r | partition.r0 | partition.r1 | partition.r2))
