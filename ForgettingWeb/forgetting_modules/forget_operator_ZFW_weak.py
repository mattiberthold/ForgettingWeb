from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_ZFW_reduct import ZFWReduction
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorZFWWeak:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        logic_program = ZFWReduction.apply(logic_program, q_literals[0:])
        logic_program = NormalizeOperator.apply(logic_program)
        result1 = LogicProgram(logic_program.get_occurrence_partition(q_literals[0]).r)
        result2 = LogicProgram(logic_program.get_occurrence_partition(q_literals[0]).r1).get_q_exclusion(q_literals[0])

        return OperatorProgramSum.apply([result1, result2])
