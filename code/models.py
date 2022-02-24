from attr import define, field

from collections import deque
from abc import abstractmethod

import tools

@define
class Solver:
    @abstractmethod
    def solve():
        pass

@define
class Problem:

    @classmethod
    def parse(cls, infile):
        # infile.readline()

        return cls()
    
    def get_max_score(self):
        return 0 

@define
class Solution:
    problem: Problem = field()
    solver: Solver = field()
    score = field(init=False, default=0)

    def __attrs_post_init__(self):
        self.score = self.calculate_score()

    def calculate_score(self):
        return tools.calculate_score(self.problem)
    
    def write(self, fh):
        fh.write(f'TODO')