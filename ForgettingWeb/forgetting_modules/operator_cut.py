from typing import List

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule
from ForgettingWeb.forgetting_modules.operator_as_dual import OperatorASDual
from ForgettingWeb.forgetting_modules.operator_program_sum import OperatorProgramSum
from ForgettingWeb.forgetting_modules.operator_rule_product import OperatorRuleProduct


class OperatorCut:
    @staticmethod
    def apply(logic_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        partition = logic_program.get_occurrence_partition(q_literal)

        new_rules = set()
        for r0 in partition.r0:
            for r4 in partition.r4:
                new_rules.add(OperatorRuleProduct.apply(r0, r4).get_q_exclusion(q_literal))
        das = OperatorASDual.apply(partition.r4 | partition.r3, q_literal)
        for r1 in partition.r1:
            for d in das:
                new_rules.add(OperatorRuleProduct.apply(r1, d).get_q_exclusion(q_literal))

        return LogicProgram(new_rules | partition.r)
