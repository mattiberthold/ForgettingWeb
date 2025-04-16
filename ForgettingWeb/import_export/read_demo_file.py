import pathlib
from typing import Tuple, Set

from ForgettingWeb.classes.literal import Literal
from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.import_export.read_input_program import read_input_program
from ForgettingWeb.import_export.read_variables_to_be_forgotten import \
    read_atoms_to_be_forgotten


def read_demo_file(file_name: str = 'demofile.txt') -> Tuple[LogicProgram, Set[Literal]]:
    resource_path = pathlib.Path().resolve().parent / 'resources'
    with open(resource_path / file_name, 'r') as read_file:
        variables_to_be_forgotten_line = read_file.readline()
        variables_to_be_forgotten = read_atoms_to_be_forgotten(variables_to_be_forgotten_line)
        program_rule_lines = read_file.readlines()
    program = read_input_program(program_rule_lines)
    return program, variables_to_be_forgotten
