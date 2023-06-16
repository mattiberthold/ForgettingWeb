from typing import Set

from forgetting_operators_logic_programming.classes.literal import Literal


class Rule:
    def __init__(self, head: Set[Literal], body_positive: Set[Literal],
                 body_negative: Set[Literal], body_negative_negative: Set[Literal]):
        self.head = head.difference({Literal('')})
        self.body_positive = body_positive.difference({Literal('')})
        self.body_negative = body_negative.difference({Literal('')})
        self.body_negative_negative = body_negative_negative.difference({Literal('')})

    def equals(self, other):
        if not self.head.__eq__(other.head):
            return False
        if not self.body_positive.__eq__(other.body_positive):
            return False
        if not self.body_negative.__eq__(other.body_negative):
            return False
        if not self.body_negative_negative.__eq__(other.body_negative_negative):
            return False
        return True

    @property
    def body_literal_strs(self) -> Set[str]:
        return {str(bp) for bp in self.body_positive} | {'~' + str(bn) for bn in self.body_negative} | \
               {'~~' + str(bnn) for bnn in self.body_negative_negative}

    @property
    def long_str(self) -> str:
        long_body_literal_str = \
            {str(bp) for bp in self.body_positive} | {'not ' + str(bn) for bn in self.body_negative} | \
            {'not not ' + str(bnn) for bnn in self.body_negative_negative}
        return '; '.join(sorted(str(head_literal) for head_literal in self.head)) + ' :- ' + \
               ', '.join(sorted(long_body_literal_str))

    @classmethod
    def from_str(cls, input_str: str):
        input_str = input_str.replace(' ', '').replace('.', '')
        if ':-' in input_str:
            # TODO check if ~~~ should be replaced by ~
            head_str, body_str = input_str.split(':-', 1)
            head_literals = {Literal(head_str_item) for head_str_item in head_str.split(';')}
            body_literal_strs = {body_str_item.strip() for body_str_item in body_str.split(',')}

            body_positive = set()
            body_negated = set()
            body_double_negated = set()
            for literal_str in body_literal_strs:
                literal_str = literal_str.replace('not', '~')
                if len(literal_str) > 0:
                    if literal_str[0] == '~':
                        if literal_str[1] == '~':
                            body_double_negated.add(Literal(literal_str[2:]))
                        else:
                            body_negated.add(Literal(literal_str[1:]))
                    else:
                        body_positive.add(Literal(literal_str))
            return cls(head_literals, body_positive, body_negated, body_double_negated)
        else:
            head_str = input_str
            head_literals = {Literal(head_str_item) for head_str_item in head_str.split(';')}
            body_positive = set()
            body_negated = set()
            body_double_negated = set()
            return cls(head_literals, body_positive, body_negated, body_double_negated)

    def __str__(self):
        return '; '.join(sorted(str(head_literal) for head_literal in self.head)) + ' :- ' + \
               ', '.join(sorted(self.body_literal_strs))

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def subsumes(self, other: 'Rule') -> bool:
        """
        Test if this rule subsumes some other rule.

        :param other: the other rule
        :return: Does this rule subsume the other rule?

        >>> Rule.from_str('a; b :- c, d').subsumes(Rule.from_str('a :- ~b, c, d'))
        True
        >>> Rule.from_str('a :- ~~b').subsumes(Rule.from_str(':- b, ~a'))
        True
        >>> Rule.from_str(':- b, ~a').subsumes(Rule.from_str('a :- ~~b'))
        False
        >>> Rule.from_str('a :- ~~b').subsumes(Rule.from_str('a :- c, ~~b'))
        True
        >>> Rule.from_str('a :- not not b').subsumes(Rule.from_str('a :- c, ~~b'))
        True
        """
        requirement_1 = self.head.issubset(other.head | other.body_negative)
        requirement_2 = self.body_positive.issubset(other.body_positive | other.body_negative_negative)
        requirement_3 = self.body_negative.issubset(other.body_negative)
        requirement_4 = self.body_negative_negative.issubset(other.body_positive | other.body_negative_negative)
        requirement_5a = not self.body_positive.intersection(other.body_negative_negative)
        requirement_5b = not self.head.intersection(other.head)
        return all([requirement_1, requirement_2, requirement_3, requirement_4]) and (requirement_5a or requirement_5b)

    def weakly_subsumes(self, other: 'Rule') -> bool:
        """
        Test if this rule subsumes some other rule.

        :param other: the other rule
        :return: Does this rule subsume the other rule?

        >>> Rule.from_str('a; b :- c, d').subsumes(Rule.from_str('a :- ~b, c, d'))
        True
        >>> Rule.from_str('a :- ~~b').subsumes(Rule.from_str(':- b, ~a'))
        True
        >>> Rule.from_str(':- b, ~a').subsumes(Rule.from_str('a :- ~~b'))
        False
        >>> Rule.from_str('a :- ~~b').subsumes(Rule.from_str('a :- c, ~~b'))
        True
        >>> Rule.from_str('a :- not not b').subsumes(Rule.from_str('a :- c, ~~b'))
        True
        """
        requirement_1 = self.head.issubset(other.head)
        requirement_2 = self.body_positive.issubset(other.body_positive)
        requirement_3 = self.body_negative.issubset(other.body_negative)
        requirement_4 = self.body_negative_negative.issubset(other.body_negative_negative)
        requirement_5 = not self.equals(other)

        return all([requirement_1, requirement_2, requirement_3, requirement_4, requirement_5])

    def copy(self) -> 'Rule':
        return Rule(self.head.copy(), self.body_positive.copy(), self.body_negative.copy(),
                    self.body_negative_negative.copy())

    def get_q_exclusion(self, q_literal: Literal) -> 'Rule':
        q_set = {q_literal}
        return Rule(self.head.copy().difference(q_set), self.body_positive.copy().difference(q_set),
                    self.body_negative.copy().difference(q_set), self.body_negative_negative.copy().difference(q_set))

    def get_double_negation(self):
        return Rule(set(), set(), self.head | self.body_negative, self.body_positive | self.body_negative_negative)

    def get_signature(self) -> Set[Literal]:
        signature = set()
        for el in self.head:
            signature.add(el)
        for el in self.body_positive:
            signature.add(el)
        for el in self.body_negative:
            signature.add(el)
        for el in self.body_negative_negative:
            signature.add(el)
        return signature
