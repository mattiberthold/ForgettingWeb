import itertools

from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.classes.rule import Rule


class NormalizeOperator:
    @staticmethod
    def _rule_is_tautology(rule: Rule):
        return rule.head.intersection(rule.body_positive) or \
               rule.body_positive.intersection(rule.body_negative) or \
               rule.body_negative.intersection(rule.body_negative_negative)

    @staticmethod
    def apply(logic_program: LogicProgram) -> LogicProgram:
        if not logic_program:
            return LogicProgram()
        # 1. Remove all tautological rules
        print(logic_program)
        keep_rules = {rule.copy() for rule in logic_program if not NormalizeOperator._rule_is_tautology(rule)}

        for keep_rule in keep_rules:
            # 2. Remove all doubly negated body parts that are already in the positive part
            keep_rule.body_negative_negative = keep_rule.body_negative_negative.difference(keep_rule.body_positive)
            # 3. Remove all atoms from the head that are in the negated part of the body
            keep_rule.head = keep_rule.head.difference(keep_rule.body_negative)

        # 4. Remove all rules that are not minimal
        remove_rules = set()
        for rule_1, rule_2 in itertools.combinations(keep_rules, 2):
            if rule_1.subsumes(rule_2):
                remove_rules.add(rule_2)
            elif rule_2.subsumes(rule_1):
                remove_rules.add(rule_1)
        keep_rules = keep_rules.difference(remove_rules)

        return LogicProgram(keep_rules)

    @staticmethod
    def apply_weak(logic_program: LogicProgram) -> LogicProgram:
        # 1. Remove all tautological rules
        keep_rules = {rule.copy() for rule in logic_program if not NormalizeOperator._rule_is_tautology(rule)}

        for keep_rule in keep_rules:
            # 2. Remove all doubly negated body parts that are already in the positive part
            keep_rule.body_negative_negative = keep_rule.body_negative_negative.difference(keep_rule.body_positive)
            # 3. Remove all atoms from the head that are in the negated part of the body
            keep_rule.head = keep_rule.head.difference(keep_rule.body_negative)

        # 4. DO NOT Remove all rules that are not minimal :)

        return LogicProgram(keep_rules)
