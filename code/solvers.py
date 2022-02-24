from attr import define

from models import Problem, Solution, Solver
import tools

@define
class SolverA(Solver):
    def solve(self, problem: Problem):
        return Solution(problem=problem, solver=self) 