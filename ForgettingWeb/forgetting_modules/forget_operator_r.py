from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_as_dual import OperatorASDual
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_program_product import OperatorProgramProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorRPositive:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(q_literal)
        a = OperatorASDual.apply(LogicProgram(occurrence_partition.r3 | occurrence_partition.r4), q_literal)
        b = LogicProgram(occurrence_partition.r0 |
                         occurrence_partition.r2).get_q_exclusion(q_literal).get_double_negation()
        c = LogicProgram(occurrence_partition.r | occurrence_partition.r2).get_q_exclusion(q_literal)
        d = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r0),
                                         LogicProgram(
                                             occurrence_partition.r3 | occurrence_partition.r4)).get_q_exclusion(
            q_literal)
        sum_logic_program = OperatorProgramSum.apply([a, b, c, d])
        return NormalizeOperator.apply(sum_logic_program)


class ForgetOperatorRNegative:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(q_literal)
        a = LogicProgram(occurrence_partition.r | occurrence_partition.r1 |
                         occurrence_partition.r4).get_q_exclusion(q_literal)
        b = LogicProgram(occurrence_partition.r1 |
                         occurrence_partition.r4).get_q_exclusion(q_literal).get_double_negation()
        sum_logic_program = OperatorProgramSum.apply([a, b])
        return NormalizeOperator.apply(sum_logic_program)


class ForgetOperatorR:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        return NormalizeOperator.apply(ForgetOperatorR.apply_(logic_program, q_literals))

    @staticmethod
    def apply_(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        if not q_literals:
            return NormalizeOperator.apply_weak(logic_program)

        product_part_1 = ForgetOperatorR.apply_(ForgetOperatorRPositive.apply(logic_program, q_literals[0]),
                                                q_literals[1:])
        product_part_2 = ForgetOperatorR.apply_(ForgetOperatorRNegative.apply(logic_program, q_literals[0]),
                                                q_literals[1:])
        return NormalizeOperator.apply_weak(OperatorProgramProduct.apply(product_part_1, product_part_2))
