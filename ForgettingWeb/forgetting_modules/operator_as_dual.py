from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule


class OperatorASDual:
    @staticmethod
    def apply(input_program: LogicProgram, q_literal: Literal) -> LogicProgram:
        result_sets = [Rule.from_str(':-')]
        for rule in input_program:
            new_sets = []
            for neg_literal in rule.head | rule.body_negative:
                if neg_literal != q_literal:
                    for other_rule in result_sets:
                        other_rule_double_negative_copy = other_rule.body_negative_negative.copy()
                        other_rule_double_negative_copy.add(neg_literal)
                        new_rule = Rule(set(), set(), other_rule.body_negative.copy(), other_rule_double_negative_copy)
                        new_sets.append(new_rule)
            for pos_literal in rule.body_positive | rule.body_negative_negative:
                if pos_literal != q_literal:
                    for other_rule in result_sets:
                        other_rule_negative_copy = other_rule.body_negative.copy()
                        other_rule_negative_copy.add(pos_literal)
                        new_rule = Rule(set(), set(), other_rule_negative_copy,
                                        other_rule.body_negative_negative.copy())
                        new_sets.append(new_rule)
            result_sets = new_sets
        return LogicProgram(set(result_sets))
