from typing import List

from ForgettingWeb.classes.logic_program import LogicProgram


class OperatorProgramSum:
    @staticmethod
    def apply(input_programs: List[LogicProgram]) -> LogicProgram:
        result_rules = {rule for input_program in input_programs for rule in input_program}
        return LogicProgram(result_rules)
