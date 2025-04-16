from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.forgetting_modules.forget_operator_sp import ForgetOperatorSP
from ForgettingWeb.forgetting_modules.operator_normalize import NormalizeOperator


class ForgetOperatorStrongAS:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]):
        # print('...')
        # print(logic_program)
        for literal in q_literals:
            # print(logic_program.get_occurrence_partition(literal).r3)
            if NormalizeOperator.apply(logic_program).get_occurrence_partition(literal).r3:
                # p-forgettablility is a bit more general this way than originally
                # print('there was a cycle')
                return logic_program, False
            else:
                logic_program = ForgetOperatorSP.apply(logic_program, [literal])
                print(logic_program)
        return logic_program, True
