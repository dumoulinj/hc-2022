import attr

from collections import deque


@attr.s
class Problem:

    @classmethod
    def parse(cls, infile):

        return cls()

@attr.s
class Solution:
    problem = attr.ib()
    solver = attr.ib()
    score = attr.ib(init=False, default=0)
    solution = attr.ib()

    # def __attrs_post_init__(self):
    #     self.score = self.calculate_score()

    def calculate_score(self):
        score = 0

        return score

    def write(self, fh):
        # TODO: Write output file here
        # fh.write("toto")
        pass