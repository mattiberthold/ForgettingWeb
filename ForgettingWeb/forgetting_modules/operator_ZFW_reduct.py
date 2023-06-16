from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.classes.rule import Rule


class ZFWReduction:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        for q_literal in q_literals:
            new_program = ZFWReduction.apply_(logic_program, q_literal)
        return new_program

    @staticmethod
    def apply_(input_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        partition = input_program.get_occurrence_partition(q_literal)

        if not partition.r4 or not partition.r0:
            return input_program

        new_rules = set()
        for r4 in partition.r4:
            for r0 in partition.r0:
                new_rules.add(Rule(r0.head | r4.head.difference(q_literal),
                                   r0.body_positive.difference(q_literal) | r4.body_positive,
                                   r0.body_negative | r4.body_negative,
                                   r0.body_negative_negative | r4.body_negative_negative))

        return LogicProgram(new_rules | partition.r | partition.r1 | partition.r2 | partition.r3)
