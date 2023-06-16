from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_EWTransformation import EWTransformation
from forgetting_operators_logic_programming.forgetting_modules.operator_as_dual import OperatorASDual
from forgetting_operators_logic_programming.forgetting_modules.operator_program_product import OperatorProgramProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorForget3:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]):
        if len(q_literals) != 1:
            return logic_program
        q = q_literals[0]

        logic_program = EWTransformation.apply(logic_program)

        logic_program = ForgetOperatorForget3.semi_shift(logic_program, q)

        partition = logic_program.get_occurrence_partition(q)
        derived = OperatorProgramProduct.apply(OperatorASDual.apply(partition.r4, q), partition.r1)

        return OperatorProgramSum.apply([derived, partition.r])

    @staticmethod
    def semi_shift(logic_program: LogicProgram, q: Literal):
        new_rules = LogicProgram()
        for rule in logic_program:
            if q in rule.head and len(rule.head) > 1:
                new_rule = rule.copy()
                new_rule.head.remove(q)
                new_rule.body_negative.add(q)
                new_rules.add(new_rule)

                new_rule = rule.copy()
                new_rule.body_negative = new_rule.body_negative.union(new_rule.head)
                new_rule.body_negative.remove(q)
                new_rule.head = {q}
                new_rules.add(new_rule)
            else:
                new_rules.add(rule)

        return new_rules
