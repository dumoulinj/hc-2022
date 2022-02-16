from copy import copy
from typing import Counter
from attr import define

from models import Problem, Solution, Solver

def calculate_score(problem: Problem, ingredients: set):
    score = 0

    for client in problem.clients:
        if ingredients >= client.likes and not ingredients & client.dislikes:
            score += 1

    return score

@define
class Naive(Solver):
    def solve(self, problem: Problem):
        liked = set()
        disliked = set()
        for c in problem:
            liked |= c.likes
            disliked |= c.dislikes

        ingredients = liked - disliked
        return Solution(problem=problem, solver=self, ingredients=ingredients)

@define
class LikesGTDislikes(Solver):
    def solve(self, problem: Problem):
        likes = Counter()
        dislikes = Counter()

        for c in problem.clients:
            likes.update(list(c.likes))
            dislikes.update(list(c.dislikes))
        
        ingredients = set()
        # not_added = set()
        
        for k, v in likes.items():
            if v >= dislikes[k]:
                ingredients.add(k)
            # else:
            #     not_added.add(k)

        # improved = True
        # while improved:
        #     improved = False
        #     not_added = problem.ingredients - ingredients
        #     for i in not_added:
        #         new_ingredients = copy(ingredients)
        #         new_ingredients.add(i)
        #         if calculate_score(problem, new_ingredients) > calculate_score(problem, ingredients):
        #             ingredients = new_ingredients
        #             improved = True
            
        #     for i in dislikes:
        #         if i in ingredients:
        #             new_ingredients = copy(ingredients)
        #             new_ingredients.remove(i)
        #             if calculate_score(problem, new_ingredients) > calculate_score(problem, ingredients):
        #                 ingredients = new_ingredients
        #                 improved = True
        
        return Solution(problem=problem, solver=self, ingredients=ingredients)


@define
class LikesGTDislikes2(Solver):
    def solve(self, problem: Problem):
        likes_counter = Counter()
        dislikes_counter = Counter()

        likes = set()
        dislikes = set()

        for c in problem.clients:
            likes_counter.update(list(c.likes))
            likes.update(c.likes)
            dislikes_counter.update(list(c.dislikes))
            dislikes.update(c.dislikes)
        
        ingredients = set()
        not_added = set()
        
        for k, v in likes_counter.items():
            if v >= dislikes_counter[k]:
                ingredients.add(k)
                # likes.remove(k)

        improved = True
        not_added = likes - ingredients
        while improved:
            improved = False
            #print(f"{len(likes)} - {len(ingredients)}, {len(not_added)}")

            crt_score = calculate_score(problem, ingredients)
            to_add = list()

            for i in not_added:
                new_ingredients = copy(ingredients)
                new_ingredients.add(i)
                new_score = calculate_score(problem, new_ingredients)
                
                if new_score > crt_score:
                    to_add.append((i, new_score))
            
            if len(to_add) > 0:
                to_add = sorted(to_add, key=lambda x: x[1], reverse=True)
                _i = to_add[0][0]
                ingredients.add(_i)
                not_added.remove(_i)
                print(f"Added score: {to_add[0][1] - crt_score}, to add length: {len(to_add)}")
                improved = True
            
            # for i in dislikes_counter:
            #     if i in ingredients:
            #         new_ingredients = copy(ingredients)
            #         new_ingredients.remove(i)
            #         if calculate_score(problem, new_ingredients) > calculate_score(problem, ingredients):
            #             ingredients = new_ingredients
            #             improved = True
        
        return Solution(problem=problem, solver=self, ingredients=ingredients)
