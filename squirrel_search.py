import random
import sys
from polynomial_calculator import polynomial_calc

num_of_dimensions = 10
num_of_agents = 50
FS_l = -0.1
FS_u = 0.1

FS = []  # flying squirrels
FS_ht = [sys.maxsize-3, None]  # flying squirrel at hickory tree (best fitness)
FS_at = [[sys.maxsize-2, None], [sys.maxsize-1, None], [sys.maxsize, None]]  # flying squirrels at acorn trees (next 3 best)


def init():
    for i in range(num_of_agents):
        FS_i = []

        for j in range(num_of_dimensions):
            FS_ij = FS_l + random.uniform(0, 1) * (FS_u - FS_l)
            FS_i.append(FS_ij)

        FS.append(FS_i)


def fitness(data, y_sum_test):
    for FS_i in FS:
        y_sum = 0

        for x in data['x']:
            y_sum += polynomial_calc(FS_i, x)

        fit = y_sum_test - y_sum  # difference between test and flying squirrel

        if fit < FS_ht[0]:  # if best fitness
            FS_ht[0] = fit
            FS_ht[1] = FS_i

        elif FS_at[0][0] > fit > FS_ht[0]:  # if second best
            FS_at[0][0] = fit
            FS_at[0][1] = FS_i

        elif FS_at[1][0] > fit > FS_at[0][0]:  # if third best
            FS_at[1][0] = fit
            FS_at[1][1] = FS_i

        elif FS_at[2][0] > y_sum > FS_at[1][0]:  # if fourth best
            FS_at[2][0] = y_sum
            FS_at[2][1] = FS_i


