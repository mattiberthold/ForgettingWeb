from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_ZFW_reduct import ZFWReduction


class ForgetOperatorZFWStrong:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        result = ZFWReduction.apply(logic_program, q_literals[0:])
        result = NormalizeOperator.apply(result)
        result = result.get_occurrence_partition(q_literals[0]).r

        return LogicProgram(result)
