from typing import List

from forgetting_operators_logic_programming.classes.logic_program import LogicProgram


class OperatorProgramSum:
    @staticmethod
    def apply(input_programs: List[LogicProgram]) -> LogicProgram:
        result_rules = {rule for input_program in input_programs for rule in input_program}
        return LogicProgram(result_rules)
