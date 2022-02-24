from attr import define, field

from collections import deque
from abc import abstractmethod


@define
class Solver:
    @abstractmethod
    def solve():
        pass


@define(frozen=True)
class Skill:
    name: str = field()
    level: int = field(converter=int)
    

@define(order=True)
class Contributor:
    name: str
    skills: list[Skill]

    def has_skill(self, skill, mentoring=False):
        if skill.level == 0:
            return True
        if skill.level == 1 and mentoring:
            return True
        for s in self.skills:
            if s.name == skill.name:
                if mentoring:
                    return s.level >= skill.level - 1
                else:
                    return s.level >= skill.level
                    

@define
class Project:
    name: str
    duration: int
    score: int
    deadline: int
    roles: list[Skill]

@define
class Assignment:
    project: Project
    contributors: list[Contributor]
    start: int = None

@define
class Problem:
    projects: list[Project] = field()
    contributors: list[Contributor] = field()
    contributors_by_skill = field(init=False, factory=dict)
    last_day: int = field(init=False)

    def __attrs_post_init__(self):
        for c in self.contributors:
            for skill in c.skills:
                self.contributors_by_skill.setdefault(skill.name, []).append((skill.level, c))

        for k, v in self.contributors_by_skill.items():
            self.contributors_by_skill[k] = sorted(v)
        
        self.last_day = max(p.deadline + p.duration for p in self.projects)

    def get_worst_contributor_for_skill(self, skill, exclude):
        contributors = self.contributors_by_skill[skill.name]
        for level, c in contributors:
            if c not in exclude and level >= skill.level:
                return c
    
    @classmethod
    def parse(cls, infile):
        nb_c, nb_p = infile.readline().strip().split(' ')
        contributors = list()
        projects = list()

        for i in range(int(nb_c)):
            name, nb_skills = infile.readline().strip().split(' ')
            skills = []
            for n in range(int(nb_skills)):
                skill_name, skill_level = infile.readline().strip().split(' ')
                skill = Skill(skill_name, int(skill_level))
                skills.append(skill)
            contributor = Contributor(name, skills)
            contributors.append(contributor)
        
        for i in range(int(nb_p)):
            project_name, nb_days, awarded_score, best_before_day, nb_roles = infile.readline().strip().split(' ')
            skills = list()
            for j in range(int(nb_roles)):
               skill_name, skill_level = infile.readline().strip().split(' ') 
               skill = Skill(skill_name, skill_level)
               skills.append(skill)
            
            project = Project(project_name, nb_days, awarded_score, best_before_day, skills)
            projects.append(project)

        return cls(projects=projects, contributors=contributors)
    
    def get_max_score(self):
        return 0 

@define
class Solution:
    problem: Problem = field()
    solver: Solver = field()
    assignments: list[Assignment] = field()
    score = field(init=False, default=0)

    def __attrs_post_init__(self):
        self.score = self.calculate_score()

    def calculate_score(self):
        import tools

        return 0
        return tools.calculate_score(self.problem)
    
    def write(self, fh):
        fh.write(f"{len(self.assignments)}\n")
        for assignment in self.assignments:
            fh.write(assignment.project.name)
            fh.write("\n")
            fh.write(" ".join(c.name for c in assignment.contributors))
            fh.write("\n")

@define
class Solution2:
    problem: Problem = field()
    solver: Solver = field()
    assignments: list[Assignment] = field()
    score = field(init=False, default=0)

    def __attrs_post_init__(self):
        self.score = self.calculate_score()

    def calculate_score(self):
        import tools
        return tools.calculate_score(self.problem)
    
    def write(self, fh):
        fh.write(f"{len(self.assignments)}\n")
        for assignment in self.assignments:
            fh.write(assignment.project.name)
            fh.write("\n")
            fh.write(" ".join(c.name for c in assignment.contributors))
            fh.write("\n")