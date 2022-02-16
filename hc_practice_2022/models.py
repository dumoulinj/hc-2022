from attr import define, field
from collections import deque
from typing import List
from abc import abstractmethod


@define
class Client:
    likes: frozenset
    dislikes: frozenset

@define
class Problem:
    clients: List[Client]
    ingredients: set

    @classmethod
    def parse(cls, infile):
        nb_clients = int(infile.readline().strip())
        clients = []
        ingredients = set()
        for i in range(nb_clients):
            likes = frozenset(infile.readline().split()[1:])
            dislikes = frozenset(infile.readline().split()[1:])
            clients.append(Client(likes, dislikes))
            ingredients.update(likes)
            ingredients.update(dislikes)

        return cls(clients=clients, ingredients=ingredients)
    
    def get_max_score(self):
        return len(self.clients)
        
    def __iter__(self):
        return iter(self.clients)


@define
class Solver:
    @abstractmethod
    def solve():
        pass


@define
class Solution:
    problem: Problem = field()
    solver: Solver = field()
    ingredients: frozenset = field()
    score = field(init=False, default=0)

    def __attrs_post_init__(self):
        self.score = self.calculate_score()

    def calculate_score(self):
        score = 0

        for client in self.problem:
            if self.ingredients >= client.likes and not self.ingredients & client.dislikes:
                score += 1

        return score
    
    def write(self, fh):
        fh.write(f'{len(self.ingredients)} {" ".join(self.ingredients)}')