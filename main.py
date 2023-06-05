import numpy as np

from ilp_solver import ILPSolver

v = np.array([[10, 10, 20, 30],
              [10, 30, 20, 30],
              [10, 40, 0, 0],
              [0, 0, 20, 30]])
z = np.array([[20, 0, 10, 20],
              [40, 4, 10, 10],
              [5, 10, 20, 0],
              [0, 10, 10, 3]])

ilp = ILPSolver(v, z)
solution = ilp.solver()
print(solution)
