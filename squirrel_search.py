import math
import random
import sys
from polynomial_calculator import polynomial_calc

num_of_dimensions = 10
num_of_agents = 50
FS_l = -0.1
FS_u = 0.1

FS = None  # flying squirrels
FS_ht = None  # flying squirrel at hickory tree (best fitness)
FS_at = None  # flying squirrels at acorn trees (next 3 best)

P_dp = 0.1  # predator presence probability (from paper)
rho = 1.204  # density of air (from paper)
V = 5.25  # velocity (from paper)
S = 0.0154  # surface area of body (from paper)
C_D = 0.6  # frictional drag coefficient (from paper)
C_L = 0.675  # lift coefficient 0.675 ≤ CL ≤ 1.5 (from paper)
h_g = 8  # loss in height occurred after gliding (from paper)
G_c = 1.9  # gliding constant (from paper)
L = 1/2 * rho * C_L * (V**2) * S  # lift (eq.8 from paper)
D = 1/2 * rho * (V**2) * S * C_D  # frictional drag (eq.9 from paper)
Phi = math.atan(D/L)  # glide angle (eq.10 from paper)
d_g = h_g / math.tan(Phi)  # gliding distance (eq.11 from paper)
sf = 18  # scaling factor (from paper)
d_g = d_g / sf  # scaled down d_q (according to paper)


def init():
    global FS, FS_ht, FS_at
    FS = []
    FS_ht = [sys.maxsize - 3, None]
    FS_at = [[sys.maxsize - 2, None], [sys.maxsize - 1, None], [sys.maxsize, None]]

    for i in range(num_of_agents):
        FS_i = []

        for j in range(num_of_dimensions):
            FS_ij = FS_l + random.uniform(0, 1) * (FS_u - FS_l)  # eq.2
            FS_i.append(FS_ij)

        FS.append(FS_i)


def fitness(data, y_sum_test):
    global FS, FS_ht, FS_at

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


