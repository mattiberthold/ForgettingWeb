from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.forgetting_modules.operator_as_dual import OperatorASDual
from ForgettingWeb.forgetting_modules.operator_normalize import NormalizeOperator
from ForgettingWeb.forgetting_modules.operator_program_product import OperatorProgramProduct
from ForgettingWeb.forgetting_modules.operator_program_sum import OperatorProgramSum
from ForgettingWeb.forgetting_modules.forget_operator_r import ForgetOperatorRNegative, ForgetOperatorRPositive


class ForgetOperatorRRPositive:
    @staticmethod
    def apply(logic_program: LogicProgram, c_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(c_literal)
        a = OperatorASDual.apply(LogicProgram(occurrence_partition.r3 | occurrence_partition.r4), c_literal)
        b = LogicProgram(occurrence_partition.r | occurrence_partition.r2)
        c = LogicProgram(occurrence_partition.r0 | occurrence_partition.r2).get_double_negation()
        # d = OperatorProgramProduct.apply(
        #     OperatorProgramProduct.apply(LogicProgram(occurrence_partition.r0),
        #                                  LogicProgram(occurrence_partition.r3 |
        #                                               occurrence_partition.r4)).get_q_exclusion(c_literal),
        #     LogicProgram({Rule(set(), set(), set(), {c_literal})}))
        d = LogicProgram(occurrence_partition.r3 | occurrence_partition.r4)
        e = LogicProgram({Rule(set(), set(), {c_literal}, set())})
        sum_logic_program = OperatorProgramSum.apply([a, b, c, d, e])
        return NormalizeOperator.apply_weak(sum_logic_program)


class ForgetOperatorRRNegative:
    @staticmethod
    def apply(logic_program: LogicProgram, c_literal: Literal) -> LogicProgram:
        occurrence_partition = logic_program.get_occurrence_partition(c_literal)
        a = LogicProgram(occurrence_partition.r | occurrence_partition.r1 | occurrence_partition.r4)
        b = LogicProgram(occurrence_partition.r1 | occurrence_partition.r4).get_double_negation()
        c = LogicProgram({Rule(set(), set(), set(), {c_literal})})
        sum_logic_program = OperatorProgramSum.apply([a, b, c])
        # sum_logic_program = OperatorProgramSum.apply([a, b])
        return NormalizeOperator.apply_weak(sum_logic_program)


class ForgetOperatorRR:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal], b_literals: List[Literal]) -> LogicProgram:
        print('\n\n new')
        c_literals = list(logic_program.get_signature().difference(b_literals).difference(q_literals))
        return NormalizeOperator.apply_weak(ForgetOperatorRR.apply_v(logic_program, q_literals, c_literals))

    @staticmethod
    def apply_c(logic_program: LogicProgram, c_literals: List[Literal]) -> LogicProgram:
        if not c_literals:
            return NormalizeOperator.apply_weak(logic_program)

        print('\n f')
        print(logic_program)
        product_part_1 = ForgetOperatorRR.apply_c(ForgetOperatorRRPositive.apply(logic_program, c_literals[0]),
                                                  c_literals[1:])
        product_part_2 = ForgetOperatorRR.apply_c(ForgetOperatorRRNegative.apply(logic_program, c_literals[0]),
                                                  c_literals[1:])
        print('\n g')
        print('product_part_1')
        print(product_part_1)
        print('product_part_2')
        print(product_part_2)
        return NormalizeOperator.apply_weak(OperatorProgramProduct.apply(product_part_1, product_part_2))

    @staticmethod
    def apply_v(logic_program: LogicProgram, q_literals: List[Literal], c_literals: List[Literal]) -> LogicProgram:
        if not q_literals:
            return ForgetOperatorRR.apply_c(logic_program, c_literals)

        product_part_1 = ForgetOperatorRR.apply_v(ForgetOperatorRPositive.apply(logic_program, q_literals[0]),
                                                  q_literals[1:], c_literals)
        product_part_2 = ForgetOperatorRR.apply_v(ForgetOperatorRNegative.apply(logic_program, q_literals[0]),
                                                  q_literals[1:], c_literals)
        return NormalizeOperator.apply_weak(OperatorProgramProduct.apply(product_part_1, product_part_2))
