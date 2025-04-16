from typing import List

from ForgettingWeb.classes.logic_program import LogicProgram
from ForgettingWeb.classes.rule import Rule


def read_input_program(input_program_str_list: List[str]) -> LogicProgram:
    program_rules = {Rule.from_str(rule_str) for rule_str in input_program_str_list if rule_str != ''}
    # program_rules = {Rule.from_str(rule_str) for rule_str in input_program_str_list
    # if ':-' in rule_str}
    return LogicProgram(program_rules)
