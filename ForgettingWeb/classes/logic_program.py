from typing import Set

from forgetting_operators_logic_programming.classes.literal import Literal
from forgetting_operators_logic_programming.classes.rule import Rule
from forgetting_operators_logic_programming.forgetting_modules.occurrence_partition import OccurrencePartition


class LogicProgram(Set[Rule]):
    def __str__(self):
        if not self:
            return 'Empty program'
        return '\n'.join(str(rule) for rule in self)

    @property
    def long_str(self):
        if not self:
            return 'Empty program'
        return '\n'.join(rule.long_str for rule in self)

    def get_q_exclusion(self, q_literal: Literal):
        return LogicProgram({rule.get_q_exclusion(q_literal) for rule in self})

    def contains_rule(self, rule: Rule) -> bool:
        return rule in list(self)

    def get_occurrence_partition(self, q_literal: Literal) -> OccurrencePartition:
        result = OccurrencePartition()
        for rule in self:
            if q_literal in rule.body_positive:
                result.r0.add(rule)
            elif q_literal in rule.body_negative:
                result.r1.add(rule)
            elif q_literal in rule.body_negative_negative:
                if q_literal in rule.head:
                    result.r3.add(rule)
                else:
                    result.r2.add(rule)
            else:
                if q_literal in rule.head:
                    result.r4.add(rule)
                else:
                    result.r.add(rule)
        return result

    def get_double_negation(self):
        double_negated_rules = [rule.get_double_negation().copy() for rule in self]
        return LogicProgram(set(double_negated_rules))

    def get_signature(self) -> Set[Literal]:
        signature = set()
        for r in self:
            signature = signature.union(r.get_signature())
        return signature
