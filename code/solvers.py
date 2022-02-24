from attr import define
from collections import defaultdict

from models import Problem, Solution, Solver, Assignment, Solution2
import tools

def get_assignmentB(problem, project, to_exclude) -> Assignment:
    contributors = [] 
    for role in project.roles:
        c = problem.get_worst_contributor_for_skill(skill=role, exclude=to_exclude)
        if not c:
            return None
        contributors.append(c)
        to_exclude.append(c)
    return Assignment(project, contributors), to_exclude

def get_assignmentA(problem, project) -> Assignment:
    contributors = [] 
    for role in project.roles:
        c = problem.get_worst_contributor_for_skill(skill=role, exclude=contributors)
        if not c:
            return None
        contributors.append(c)
    return Assignment(project, contributors)


def get_assignment_matrix(problem, project, contributors):
    roles = {}

    for role in project.roles:
        roles[role] = []
        for contributor in contributors:
            if contributor.has_skill(role, mentoring=False):
                roles[role].append(contributor)
        if not roles[role]:
            print("Cannot pick project")
            return

    print(roles)

    selected = {}
    
    def get_other_possible_assignments(contributor, role, by_availability):
        count = 0
        for other_role, contributors in by_availability.items():
            for c in contributors:
                if c == contributor:
                    count += 1
        return count

    while roles:
        role, contributors = min(roles.items(), key=lambda i: len(i[1]))
        del roles[role]

        contributor = min(
            contributors,
            key=lambda c: get_other_possible_assignments(c, role, roles),
        )

        selected[role] = contributor

        for contributors in roles.values():
            remove = False
            for i, c in enumerate(contributors):
                if c == contributor:
                    remove = True
                    break
            if remove:
                contributors.pop(i)
            if not contributors:
                print("Cannot pick project")
                return

    assignment = []
    for role in project.roles:
        assignment.append(selected[role])

    return Assignment(project, assignment)
        
                    

@define
class SolverA(Solver):
    def solve(self, problem: Problem):
        assignments = []

        for project in problem.projects:
            assignment = get_assignment_matrix(problem, project, problem.contributors) 
            if not assignment:
                continue
            assignments.append(assignment)
        
        return Solution(problem=problem, solver=self, assignments=assignments) 


@define
class SolverB(Solver):
    def solve(self, problem: Problem):
        assignments = []

        # Iterate in a different way in projects
            # sort them by score
            # move two projects away if same skills needed
        def get_sort_value(project):
            return self.score / self.duration


        projects = sorted(problem.projects, key=get_sort_value, reverse=True)

        for project in projects:
            assignment = get_assignmentA(problem, project)
            if not assignment:
                continue
            assignments.append(assignment)
        
        return Solution(problem=problem, solver=self, assignments=assignments) 

@define
class SolverCollaboration(Solver):
    def solve(self, problem: Problem):
        assignments = []

        # Iterate in a different way in projects
            # sort them by score
            # move two projects away if same skills needed
        projects = sorted(problem.projects, key=lambda p: p.score, reverse=True)

        for project in projects:
            assignment = get_assignmentA(problem, project)
            if not assignment:
                continue
            assignments.append(assignment)
        
        return Solution(problem=problem, solver=self, assignments=assignments) 

@define
class SolverSim(Solver):
    def solve(self, problem: Problem):
        assignments = []

        # Iterate in a different way in projects
            # sort them by score
            # move two projects away if same skills needed
        def get_sort_value(project):
            return self.score / self.duration


        projects = sorted(problem.projects, key=get_sort_value, reverse=True)

        time = 0
        busy_contributors = set()
        available_contributors = set(problem.contributors)
        to_end = defaultdict(list())

        while time <= problem.last_day:
            finished = to_end[time]
            for a in finished:
                available_contributors.extend(a.contributors)

            project = projects.pop(0)
            while project:
                if projects.deadline + project.duration + time <= problem.last_day: 
                    assignment, busy_contributors = get_assignmentB(problem, project, busy_contributors)
                    available_contributors = available_contributors - busy_contributors

                    if assignment:
                        assignment.start = time
                        assignments.append(assignment)
                        to_end[time + assignment.project.duration].append(assignment)
                    else:
                        projects.append(project)
                project = projects.pop(0)
            time += 1
        
        return Solution2(problem=problem, solver=self, assignments=assignments) 