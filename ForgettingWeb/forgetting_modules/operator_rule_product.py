from ForgettingWeb.classes.rule import Rule


class OperatorRuleProduct:
    @staticmethod
    def apply(rule1: Rule, rule2: Rule) -> Rule:
        return Rule(
            rule1.head | rule2.head,
            rule1.body_positive | rule2.body_positive,
            rule1.body_negative | rule2.body_negative,
            rule1.body_negative_negative | rule2.body_negative_negative
        )
