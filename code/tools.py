from queue import PriorityQueue

from models import Problem, Assignment

def calculate_score(problem: Problem, assignments: list[Assignment]):
    score = 0

    for a in assignments:
        penalty = max(0, (a.start + a.duration) - a.deadline)
        score += a.project.score - penalty

    # time = 0
    # events = PriorityQueue()
    # available = set(problem.contributors)
    # reserved = set()

    # for assignment in assignments:
    #     needed = set(assignment.contributors)
    #     while needed > available:
    #         time, completed_assignment = events.get()
    #         available += completed_assignment.contributors
    #         # TODO: Add to score
            
    #     available -= assignment.contributors
    #     project_ends = time + assignment.project.duration
    #     events.put((project_ends, assignment))
                
    return score