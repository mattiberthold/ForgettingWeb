from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_r import ForgetOperatorR
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_w import ForgetOperatorW
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorSPs:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        result_forget_operator_r = ForgetOperatorR.apply(logic_program, q_literals)
        result_forget_operator_w = ForgetOperatorW.apply(logic_program, q_literals)
        return NormalizeOperator.apply(OperatorProgramSum.apply([result_forget_operator_r, result_forget_operator_w]))
