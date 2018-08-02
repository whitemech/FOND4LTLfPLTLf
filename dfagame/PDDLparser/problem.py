from dfagame.PDDLparser.formula import FormulaOr
import itertools

class Problem(object):

    def __init__(self, name, domain, objects, init, goal):
        self._name = name
        self._domain = domain
        self._objects = {}
        for obj in objects:
            self._objects[obj.type] = self._objects.get(obj.type, [])
            self._objects[obj.type].append(str(obj.value))
        self._init = set(map(str, init))
        self._goal = set(map(str, goal))

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def objects(self):
        return self._objects.copy()

    @property
    def init(self):
        return self._init.copy()

    @property
    def goal(self):
        return self._goal.copy()

    def __str__(self):
        problem_str  = '(define (problem {0})\n'.format(self._name)
        problem_str += '\t(:domain {0})\n'.format(self._domain)
        problem_str += '\t(:objects '
        for type, objects in self._objects.items():
            problem_str += '{0} - {1}'.format(' '.join(sorted(objects)), type)
        problem_str += ')\n'
        problem_str += '\t(:init {0})\n'.format(' '.join(sorted(self._init)))
        problem_str += '(:goal (and {0}))\n'.format(' '.join(sorted(self._goal)))
        problem_str += ')'
        return problem_str

    def make_new_init(self):
        self._init.add('(turnDomain)')
        self._init.add('(= q 1)')
        return self._init

    def make_new_goal(self, final_states):
        self._goal.add('(turnDomain)')
        if len(final_states) > 1:
            or_list = []
            for state in final_states:
                or_list.append('(= q {0})'.format(str(state)))
            new_formula = FormulaOr(or_list)
            self._goal.add(str(new_formula))
        else:
            self._goal.add('(= q {0})'.format(final_states[0]))

    def get_new_problem(self, final_states):
        self.make_new_init()
        self.make_new_goal(final_states)
        return self.__str__()