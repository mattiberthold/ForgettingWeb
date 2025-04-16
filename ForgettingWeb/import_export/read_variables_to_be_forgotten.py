from typing import List

from ForgettingWeb.classes.literal import Literal


def read_atoms_to_be_forgotten(input_str: str) -> List[Literal]:
    forgotten_atoms = []
    for atom in input_str.split(','):
        forgotten_atoms.append(Literal(atom.strip()))
    return forgotten_atoms

