import itertools
from typing import List

from forgetting_operators_logic_programming.classes.logic_program import LogicProgram
from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.rule import Rule


class EWTransformation:

    @staticmethod
    def _rule_is_tautology(rule: Rule):
        return rule.head.intersection(rule.body_positive) or \
            rule.body_positive.intersection(rule.body_negative) or \
            rule.body_negative.intersection(rule.body_negative_negative)

    @staticmethod
    def _unfold(input_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        partition = input_program.get_occurrence_partition(q_literal)
        if not partition.r4 or not partition.r0:
            return input_program
        new_rules = set()
        for r4 in partition.r4:
            for r0 in partition.r0:
                new_rules.add(Rule(r0.head | r4.head.difference(q_literal),
                                   r0.body_positive.difference(q_literal) | r4.body_positive,
                                   r0.body_negative | r4.body_negative,
                                   r0.body_negative_negative | r4.body_negative_negative))

            return LogicProgram(new_rules | partition.r | partition.r1 | partition.r4)

    @staticmethod
    def apply(input_program: LogicProgram) -> LogicProgram:
        # 1. Remove all tautological rules
        keep_rules = {rule.copy() for rule in input_program if not EWTransformation._rule_is_tautology(rule)}

        for keep_rule in keep_rules:
            # 3. Remove all atoms from the head that are in the negated part of the body
            keep_rule.head = keep_rule.head.difference(keep_rule.body_negative)

        # Normalization
        remove_rules = set()
        for rule_1, rule_2 in itertools.combinations(keep_rules, 2):
            if rule_1.weakly_subsumes(rule_2):
                remove_rules.add(rule_2)
            elif rule_2.weakly_subsumes(rule_1):
                remove_rules.add(rule_1)
        keep_rules = keep_rules.difference(remove_rules)

        keep_rules = LogicProgram(keep_rules)

        signature = keep_rules.get_signature()
        not_in_head = set()

        for atom in signature:
            for rule in keep_rules:
                if atom in rule.head:
                    not_in_head.add(atom)

        for rule in keep_rules:
            rule.body_negative = rule.body_negative.difference(not_in_head)

        signature = keep_rules.get_signature()

        # unfolding
        for atom in signature:
            keep_rules = EWTransformation._unfold(keep_rules, atom)

        return keep_rules
