from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_cut import OperatorCut
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_semi_shift import OperatorSemiShift
from forgetting_operators_logic_programming.semantic_modules.forget_operator_sem_up import ForgetOperatorSemUP
from forgetting_operators_logic_programming.semantic_modules.ht_model import ClassicalInterpretation
from forgetting_operators_logic_programming.semantic_modules.lp_to_models import LP2Models
from forgetting_operators_logic_programming.semantic_modules.models_to_lp import Models2LP
from forgetting_operators_logic_programming.semantic_modules.sem_forgetting_instance import SemForgettingInstance


class ForgetOperatorUniform:
    @staticmethod
    def apply(logic_program: LogicProgram, v_literals: List[Literal]):
        done = set()
        for q in v_literals:
            logic_program = NormalizeOperator.apply(logic_program)
            partition = logic_program.get_occurrence_partition(q)
            if partition.r3:
                break
            done.add(q)
            logic_program = OperatorSemiShift.apply(logic_program, [q])

            logic_program = OperatorCut.apply(logic_program, q)

        v_literals = set(v_literals).difference(done)
        if len(v_literals) > 0:
            y_wo_v_literals = ClassicalInterpretation(logic_program.get_signature().difference(v_literals))
            instance = SemForgettingInstance(LP2Models.apply(logic_program), y_wo_v_literals,
                                             ClassicalInterpretation(v_literals))
            return Models2LP.apply(ForgetOperatorSemUP.apply(instance), y_wo_v_literals)

        return NormalizeOperator.apply(logic_program)
