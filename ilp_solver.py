import numpy as np
from ortools.linear_solver import pywraplp


class ILPSolver:
    """
    sum(p(i, j, k), i, j, k) -> max
    sum(p(i, j, k), k) <= v(i, j),
    sum(p(i, j, k), i) <= z(k, j),
    """

    @classmethod
    def validation_type(cls, arg):
        if isinstance(arg, np.ndarray):
            return True

    def __init__(self, v, z):
        data = (v, z)
        if all(map(lambda element: self.validation_type(element), data)):
            self.v = v
            self.z = z

    def solver(self):
        solver = pywraplp.Solver('Max', pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
        x = {}
        for i in range(len(self.v)):
            for j in range(len(self.v[i])):
                for k in range(len(self.z)):
                    x[i, j, k] = solver.IntVar(0, solver.infinity(), 'x' + str(i) + str(j) + str(k))

        for i in range(len(self.v)):
            for j in range(len(self.v[i])):
                solver.Add(solver.Sum([x[i, j, k] for k in range(len(self.z))]) <= self.v[i][j]/3)

        for k in range(len(self.z)):
            for j in range(len(self.v[0])):
                solver.Add(solver.Sum([x[i, j, k] for i in range(len(self.v))]) <= self.z[k][j]/3)

        objective_function = []
        for i in range(len(self.v)):
            for j in range(len(self.v[i])):
                for k in range(len(self.z)):
                    objective_function.append(x[i, j, k])

        solver.Maximize(solver.Sum(objective_function))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            p = np.zeros((len(self.v), len(self.v[0]), len(self.z)))
            for i in range(len(self.v)):
                for j in range(len(self.v[i])):
                    for k in range(len(self.z)):
                        p[i][j][k] = 3 * x[i, j, k].solution_value()
            func = np.sum([[[p[i][j][k] for k in range(len(self.z))]
                            for j in range(len(self.v[i]))]
                           for i in range(len(self.v))])
            return p, func
        else:
            print('The solver could not find an optimal solution')
