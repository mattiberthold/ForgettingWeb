from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.semantic_modules.forget_operator_sem_sp import ForgetOperatorSemSP
from forgetting_operators_logic_programming.semantic_modules.forget_operator_sem_r import ForgetOperatorSemR
from forgetting_operators_logic_programming.semantic_modules.forget_operator_sem_m import ForgetOperatorSemM
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation
from forgetting_operators_logic_programming.semantic_modules.lp_to_models import LP2Models
from forgetting_operators_logic_programming.semantic_modules.sem_forgetting_instance import SemForgettingInstance
from forgetting_operators_logic_programming.semantic_modules.models_to_lp import Models2LP


class ForgetOperatorSemanticWrapper:
    @staticmethod
    def apply_sem_sp(logic_program: LogicProgram, v_literals: List[Literal]) -> LogicProgram:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemForgettingInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                         ClassicalInterpretation(v_literals))
        return Models2LP.apply(ForgetOperatorSemSP.apply(instance), y_wo_v_literals)

    @staticmethod
    def apply_sem_r(logic_program: LogicProgram, v_literals: List[Literal]) -> LogicProgram:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemForgettingInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                         ClassicalInterpretation(v_literals))
        return Models2LP.apply(ForgetOperatorSemR.apply(instance), y_wo_v_literals)

    @staticmethod
    def apply_sem_m(logic_program: LogicProgram, v_literals: List[Literal]) -> LogicProgram:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemForgettingInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                         ClassicalInterpretation(v_literals))
        return Models2LP.apply(ForgetOperatorSemM.apply(instance), y_wo_v_literals)

