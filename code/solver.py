from attr import define
from abc import abstractmethod


@define
class Solver:
    @abstractmethod
    def solve():
        pass

@define
class SolverA(Solver):
    def solve(self, problem):
        return self.solution