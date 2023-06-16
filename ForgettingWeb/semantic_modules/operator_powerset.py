from itertools import chain, combinations


class OperatorPowerset:
    @staticmethod
    def apply(iterable):
        s = list(iterable)
        list_of_tuples = set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

        out = set({})
        for el in list_of_tuples:
            out.add(frozenset(list(el)))
        return out
