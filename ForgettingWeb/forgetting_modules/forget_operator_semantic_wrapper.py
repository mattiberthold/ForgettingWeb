from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.forgetting_modules.forget_operator_rSP import ForgetOperatorRSP
from ForgettingWeb.forgetting_modules.forget_operator_rR import ForgetOperatorRR
from ForgettingWeb.semantic_modules.forget_operator_sem_rR import ForgetOperatorSemrR
from ForgettingWeb.semantic_modules.forget_operator_sem_rSP import ForgetOperatorSemrSP
from ForgettingWeb.semantic_modules.forget_operator_sem_sp import ForgetOperatorSemSP
from ForgettingWeb.semantic_modules.forget_operator_sem_r import ForgetOperatorSemR
from ForgettingWeb.semantic_modules.forget_operator_sem_m import ForgetOperatorSemM
from ForgettingWeb.semantic_modules.ht_model import ClassicalInterpretation
from ForgettingWeb.semantic_modules.lp_to_models import LP2Models
from ForgettingWeb.semantic_modules.sem_forgetting_instance import SemForgettingInstance
from ForgettingWeb.semantic_modules.sem_rel_forget_instance import SemRelForgetInstance
from ForgettingWeb.semantic_modules.models_to_lp import Models2LP


class ForgetOperatorSemanticWrapper:

    @staticmethod
    def apply_sem_rR(logic_program: LogicProgram, v_literals: List[Literal], b_literals: List[Literal]) -> LogicProgram:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemRelForgetInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                        ClassicalInterpretation(v_literals), ClassicalInterpretation(b_literals))
        return Models2LP.apply(ForgetOperatorSemrR.apply(instance), y_wo_v_literals)

    @staticmethod
    def apply_sem_rSP(logic_program: LogicProgram, v_literals: List[Literal], b_literals: List[Literal]) -> LogicProgram:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemRelForgetInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                        ClassicalInterpretation(v_literals), ClassicalInterpretation(b_literals))
        return Models2LP.apply(ForgetOperatorSemrSP.apply(instance), y_wo_v_literals)

    @staticmethod
    def apply_rSP_test(logic_program: LogicProgram, v_literals: List[Literal], b_literals: List[Literal])\
            -> tuple[LogicProgram, LogicProgram, LogicProgram, bool]:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemRelForgetInstance(LP2Models.apply(logic_program),
                                        y_wo_v_literals,
                                        ClassicalInterpretation(v_literals),
                                        ClassicalInterpretation(b_literals))

        syn_result = ForgetOperatorRSP.apply(logic_program, v_literals, b_literals)
        sem_result = ForgetOperatorSemrSP.apply(instance)
        syn_result_normalized = Models2LP.apply(LP2Models.apply_fixed_signature(syn_result, y_wo_v_literals),
                                                set(y_wo_v_literals))
        sem_result = Models2LP.apply(sem_result, set(y_wo_v_literals))

        return syn_result, syn_result_normalized, sem_result, syn_result_normalized == sem_result

    @staticmethod
    def apply_rR_test(logic_program: LogicProgram, v_literals: List[Literal], b_literals: List[Literal])\
            -> tuple[LogicProgram, LogicProgram, LogicProgram, bool]:
        y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
        instance = SemRelForgetInstance(LP2Models.apply(logic_program),
                                        y_wo_v_literals,
                                        ClassicalInterpretation(v_literals),
                                        ClassicalInterpretation(b_literals))

        syn_result = ForgetOperatorRR.apply(logic_program, v_literals, b_literals)
        sem_result = ForgetOperatorSemrR.apply(instance)

        syn_result_normalized = Models2LP.apply(LP2Models.apply_fixed_signature(syn_result, y_wo_v_literals),
                                                set(y_wo_v_literals))
        sem_result = Models2LP.apply(sem_result, set(y_wo_v_literals))

        return syn_result, syn_result_normalized, sem_result, syn_result_normalized == sem_result

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
