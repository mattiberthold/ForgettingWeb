from typing import List

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.rule import Rule
from forgetting_operators_logic_programming.forgetting_modules.operator_as_dual import OperatorASDual
from forgetting_operators_logic_programming.forgetting_modules.operator_rule_product import OperatorRuleProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_program_sum import OperatorProgramSum
from forgetting_operators_logic_programming.forgetting_modules.operator_program_product import OperatorProgramProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_program_product import OperatorRuleProduct
from forgetting_operators_logic_programming.forgetting_modules.operator_normalize import NormalizeOperator


class ForgetOperatorSP:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literals: List[Literal]) -> LogicProgram:
        for q in q_literals:
            logic_program = ForgetOperatorSP.apply_(logic_program, q)
        return NormalizeOperator.apply(logic_program)

    @staticmethod
    def apply_(logic_program: LogicProgram, q: Literal):
        logic_program = NormalizeOperator.apply(logic_program)
        partition = logic_program.get_occurrence_partition(q)
        result = LogicProgram()
        for r0 in partition.r0:
            # derivation 1a
            for r4 in partition.r4:
                result.add(OperatorRuleProduct.apply(r0, r4))
            # derivation 2a
            for r3 in partition.r3:
                for rp in partition.r1 | partition.r4:
                    rule = OperatorRuleProduct.apply(r0, r3)
                    rule = OperatorRuleProduct.apply(rule, rp.get_double_negation())
                    result.add(rule)
            # derivation 3a (and 7)
            for d in OperatorASDual.apply(partition.r0 | partition.r2, q):
                for r3 in partition.r3:
                    for r3p in partition.r3:
                        rule = OperatorRuleProduct.apply(r0, r3)
                        rule = OperatorRuleProduct.apply(rule, r3p.get_double_negation())
                        rule = OperatorRuleProduct.apply(rule, d)
                        result.add(rule)

        for r2 in partition.r2:
            # derivation 1b
            for r4 in partition.r4:
                result.add(OperatorRuleProduct.apply(r2, r4.get_double_negation()))
            # derivation 2b
            for r3 in partition.r3:
                for rp in partition.r1 | partition.r4:
                    rule = OperatorRuleProduct.apply(r2, r3.get_double_negation())
                    rule = OperatorRuleProduct.apply(rule, rp.get_double_negation())
                    result.add(rule)
            # derivation 3b
            for d in OperatorASDual.apply(partition.r0 | partition.r2, q):
                for r3 in partition.r3:
                    rule = OperatorRuleProduct.apply(r2, r3.get_double_negation())
                    rule = OperatorRuleProduct.apply(rule, d)
                    result.add(rule)

        for rp in partition.r1 | partition.r4:
            # derivation 4
            for d in OperatorASDual.apply(partition.r3 | partition.r4, q):
                result.add(OperatorRuleProduct.apply(rp, d))
            for r3 in partition.r3:
                # derivation 5
                for r in partition.r0 | partition.r2:
                    for d in OperatorASDual.apply(partition.r4, q):
                        rule = OperatorRuleProduct.apply(rp, r.get_double_negation())
                        rule = OperatorRuleProduct.apply(rule, r3.get_double_negation())
                        rule = OperatorRuleProduct.apply(rule, d)
                        result.add(rule)
                # derivation 6
                for d in OperatorASDual.apply(partition.r1 | partition.r4, q):
                    rule = OperatorRuleProduct.apply(rp, r3.get_double_negation())
                    rule = OperatorRuleProduct.apply(rule, d)
                    result.add(rule)

        return result.get_q_exclusion(q)
