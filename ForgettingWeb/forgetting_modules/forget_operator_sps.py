from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.forgetting_modules.forget_operator_r import ForgetOperatorR
from ForgettingWeb.forgetting_modules.forget_operator_w import ForgetOperatorW
from ForgettingWeb.forgetting_modules.operator_normalize import NormalizeOperator
from ForgettingWeb.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorSPs:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        result_forget_operator_r = ForgetOperatorR.apply(logic_program, q_literals)
        result_forget_operator_w = ForgetOperatorW.apply(logic_program, q_literals)
        return NormalizeOperator.apply(OperatorProgramSum.apply([result_forget_operator_r, result_forget_operator_w]))
