from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.forgetting_modules.forget_operator_rR import ForgetOperatorRR
from ForgettingWeb.forgetting_modules.forget_operator_w import ForgetOperatorW
from ForgettingWeb.forgetting_modules.forget_operator_w import ForgetOperatorWNegative
from ForgettingWeb.forgetting_modules.forget_operator_w import ForgetOperatorWPositive
from ForgettingWeb.forgetting_modules.operator_normalize import NormalizeOperator
from ForgettingWeb.forgetting_modules.operator_program_product import OperatorProgramProduct
from ForgettingWeb.forgetting_modules.operator_program_sum import OperatorProgramSum
from ForgettingWeb.forgetting_modules.operator_as_dual import OperatorASDual


class ForgetOperatorRSP:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal], b_literals: List[Literal]) -> LogicProgram:
        result_forget_operator_rR = ForgetOperatorRR.apply(logic_program, q_literals, b_literals)
        result_forget_operator_rW = ForgetOperatorRW.apply(logic_program, q_literals, b_literals)
        return NormalizeOperator.apply(OperatorProgramSum.apply([result_forget_operator_rR, result_forget_operator_rW]))


class ForgetOperatorRWPositive:
    @staticmethod
    def apply(logic_program: LogicProgram, c_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(c_literal)
        # a_product_1 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r0),
        #                                            LogicProgram(occurrence_partition.r3 |
        #                                                         occurrence_partition.r4)).get_q_exclusion(c_literal)
        # a_product_2 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r3 |
        #                                                         occurrence_partition.r4).get_double_negation(),
        #                                            OperatorASDual.apply(
        #                                                LogicProgram(occurrence_partition.r0 | occurrence_partition.r2),
        #                                                c_literal)).get_q_exclusion(c_literal)
        # a_product_3 = LogicProgram({Rule(set(), set(), set(), {c_literal})})
        # a = OperatorProgramProduct.apply(OperatorProgramProduct.apply(a_product_1, a_product_2), a_product_3)
        a_product_1 = LogicProgram(occurrence_partition.r3 | occurrence_partition.r4).get_q_exclusion(c_literal)
        a_product_2 = LogicProgram(occurrence_partition.r3 | occurrence_partition.r4).get_double_negation()
        a_product_3 = OperatorASDual.apply(LogicProgram(occurrence_partition.r0 | occurrence_partition.r2), c_literal)
        a = OperatorProgramProduct.apply(OperatorProgramProduct.apply(a_product_1, a_product_2), a_product_3)

        b_product_1 = OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r | occurrence_partition.r2),
                                                   LogicProgram(occurrence_partition.r3 |
                                                                occurrence_partition.r4).get_double_negation())
        b_product_2 = OperatorASDual.apply(LogicProgram(occurrence_partition.r0 | occurrence_partition.r2), c_literal)
        b = OperatorProgramProduct.apply(b_product_1, b_product_2)

        return NormalizeOperator.apply(OperatorProgramSum.apply([a, b]))


class ForgetOperatorRWNegative:
    @staticmethod
    def apply(logic_program: LogicProgram, c_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(c_literal)
        a_product_1 = LogicProgram(occurrence_partition.r | occurrence_partition.r1 | occurrence_partition.r4)
        a_product_2 = OperatorASDual.apply(LogicProgram(occurrence_partition.r1 | occurrence_partition.r4), c_literal)
        a = OperatorProgramProduct.apply(a_product_1, a_product_2)
        return NormalizeOperator.apply(a)


class ForgetOperatorRW:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal], b_literals: List[Literal]) -> LogicProgram:
        c_literals = list(logic_program.get_signature().difference(b_literals).difference(q_literals))
        return ForgetOperatorRW.apply_v(logic_program, q_literals, c_literals)

    @staticmethod
    def apply_c(logic_program: LogicProgram, c_literals: List[Literal]) -> LogicProgram:
        if not c_literals:
            return NormalizeOperator.apply(logic_program)
        product_part_1 = ForgetOperatorRW.apply_c(ForgetOperatorRWPositive.apply(logic_program, c_literals[0]),
                                                  c_literals[1:])
        product_part_2 = ForgetOperatorRW.apply_c(ForgetOperatorRWNegative.apply(logic_program, c_literals[0]),
                                                  c_literals[1:])
        return NormalizeOperator.apply_weak(OperatorProgramProduct.apply(product_part_1, product_part_2))

    @staticmethod
    def apply_v(logic_program: LogicProgram, q_literals: List[Literal], c_literals: List[Literal]) -> LogicProgram:
        if not q_literals:
            return ForgetOperatorRW.apply_c(logic_program, c_literals)

        product_part_1 = ForgetOperatorRW.apply_v(ForgetOperatorWPositive.apply(logic_program, q_literals[0]),
                                                  q_literals[1:], c_literals)
        product_part_2 = ForgetOperatorRW.apply_v(ForgetOperatorWNegative.apply(logic_program, q_literals[0]),
                                                  q_literals[1:], c_literals)
        return NormalizeOperator.apply(OperatorProgramSum.apply([product_part_1, product_part_2]))
