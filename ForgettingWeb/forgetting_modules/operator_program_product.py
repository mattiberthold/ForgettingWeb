from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.forgetting_modules.operator_rule_product import OperatorRuleProduct


class OperatorProgramProduct:
    @staticmethod
    def apply(logic_program1: LogicProgram, logic_program2: LogicProgram):
        result_program_rules = [OperatorRuleProduct.apply(rule_1, rule_2).copy()
                                for rule_1 in logic_program1
                                for rule_2 in logic_program2]
        return LogicProgram(set(result_program_rules))
