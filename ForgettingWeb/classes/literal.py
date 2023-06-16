class Literal(str):
    def __init__(self, literal_str: str):
        str.__init__(literal_str.strip())

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
