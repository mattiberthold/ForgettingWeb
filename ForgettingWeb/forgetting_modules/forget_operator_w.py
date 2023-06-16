from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_as_dual import OperatorASDual
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator
from forgetting_operators_logic_programming.forgetting_modules.operator_program_product import OperatorProgramProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum


class ForgetOperatorWPositive:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(q_literal)
        a_product_1 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r0),
                                                   LogicProgram(occurrence_partition.r3 | occurrence_partition.r4))
        a_product_2 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r3 |
                                                                occurrence_partition.r4).get_double_negation(),
                                                   OperatorASDual.apply(
                                                       LogicProgram(occurrence_partition.r0 | occurrence_partition.r2),
                                                       q_literal))
        a = OperatorProgramProduct.apply(a_product_1, a_product_2).get_q_exclusion(q_literal)

        b_product_1 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r | occurrence_partition.r2),
                                                   LogicProgram(occurrence_partition.r3 |
                                                                occurrence_partition.r4).get_double_negation())
        b_product_2 = OperatorASDual.apply(LogicProgram(occurrence_partition.r0 | occurrence_partition.r2), q_literal)
        b = OperatorProgramProduct.apply(b_product_1, b_product_2).get_q_exclusion(q_literal)

        return NormalizeOperator.apply(OperatorProgramSum.apply([a, b]))


class ForgetOperatorWNegative:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(q_literal)
        a_product_1 = LogicProgram(occurrence_partition.r | occurrence_partition.r1 | occurrence_partition.r4)
        a_product_2 = OperatorASDual.apply(LogicProgram(occurrence_partition.r1 | occurrence_partition.r4), q_literal)
        a = OperatorProgramProduct.apply(a_product_1, a_product_2).get_q_exclusion(q_literal)
        return NormalizeOperator.apply(a)


class ForgetOperatorW:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        if not q_literals:
            return NormalizeOperator.apply(logic_program)

        product_part_1 = ForgetOperatorW.apply(ForgetOperatorWPositive.apply(logic_program, q_literals[0]),
                                               q_literals[1:])
        product_part_2 = ForgetOperatorW.apply(ForgetOperatorWNegative.apply(logic_program, q_literals[0]),
                                               q_literals[1:])
        return NormalizeOperator.apply(OperatorProgramSum.apply([product_part_1, product_part_2]))
