import math
import random
import sys
from scipy.stats import truncnorm
from polynomial_calculator import polynomial_calc


class Variables(object):
    num_of_dimensions = None
    num_of_agents = None
    FS_nt_to_at = None  # probability of flying squirrels at normal trees moving towards acorn trees

    FS_l = None  # lower bound
    FS_u = None  # upper bound

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


var = Variables()  # holding all variables


def squirrel_search(fitness_func, fitness_data=None, num_of_agents=50, num_of_iters=50, num_of_dims=10, FS_l = -0.1,
                    FS_u = 0.1, FS_nt_to_at = 0.05):
    global var
    var.num_of_dimensions = num_of_dims
    var.num_of_agents = num_of_agents
    var.FS_l = FS_l
    var.FS_u = FS_u
    var.FS_nt_to_at = FS_nt_to_at
    FS_ht_evolution = []

    init(fitness_func, fitness_data)

    for i in range(num_of_iters):
        FS_ht_evolution.append(var.FS_ht.fit)  # add best squirrel (for showing evolution in time)

        # squirrels on normal trees
        for FS_nt_i in var.FS:
            # skip squirrels on other than normal tree
            if FS_nt_i == var.FS_ht or FS_nt_i in var.FS_at:
                continue

            # squirrels on normal trees moving towards acorn nut tree
            if random.uniform(0, 1) >= var.FS_nt_to_at:
                if random.uniform(0, 1) >= var.P_dp:
                    at_i = random.randint(0, 2)
                    for j in range(num_of_dims):
                        FS_nt_i.pos[j] = FS_nt_i.pos[j] + var.d_g * var.G_c * (var.FS_at[at_i].pos[j] - FS_nt_i.pos[j])  # eq.5ab
                else:
                    FS_nt_i.pos = random_location()

                FS_nt_i.fit = fitness_func(fitness_data, FS_nt_i)
            # squirrels on normal trees moving towards hickory nut tree
            else:
                if random.uniform(0, 1) >= var.P_dp:
                    for j in range(num_of_dims):
                        FS_nt_i.pos[j] = FS_nt_i.pos[j] + var.d_g * var.G_c * (var.FS_ht.pos[j] - FS_nt_i.pos[j])  # eq.6ab
                else:
                    FS_nt_i.pos = random_location()

                FS_nt_i.fit = fitness_func(fitness_data, FS_nt_i)

        # squirrels on acorn trees moving towards hickory nut tree
        for FS_at_i in var.FS_at:
            if random.uniform(0, 1) >= var.P_dp:
                for j in range(num_of_dims):
                    FS_at_i.pos[j] = FS_at_i.pos[j] + var.d_g * var.G_c * (var.FS_ht.pos[j] - FS_at_i.pos[j])  # eq.4ab
            else:
                FS_at_i.pos = random_location()

            FS_at_i.fit = fitness_func(fitness_data, FS_at_i)

        # calculate seasonal constant
        S_c_part = 0
        for FS_at_i in var.FS_at:
            pos_dif = 0
            for j in range(num_of_dims):
                pos_dif += FS_at_i.pos[j] - var.FS_ht.pos[j]

            S_c_part += pos_dif**2

        S_c = math.sqrt(S_c_part)  # eq.12

        S_min = (10**(-5)) / (365**(i/(num_of_iters/2.5)))  # eq.13

        # check the seasonal monitoring condition
        if S_c < S_min:
            # randomly relocate flying squirrels using Eq. (14)
            for FS_nt_i in var.FS:
                # skip squirrel on hickory tree (best squirrel)
                if FS_nt_i == var.FS_ht:
                    continue
                FS_nt_i.pos = levy_relocation()
                FS_nt_i.fit = fitness_func(fitness_data, FS_nt_i)

        set_best_squirrels()

    return var.FS_ht, FS_ht_evolution


def init(fitness_func, fitness_data):
    global var
    var.FS = []
    var.FS_ht = FlyingSquirrel()
    var.FS_ht.fit = sys.maxsize - 3
    var.FS_at = []
    for i in reversed(range(3)):
        fs = FlyingSquirrel
        fs.fit = sys.maxsize - i
        var.FS_at.append(fs)

    for i in range(var.num_of_agents):
        FS_i = FlyingSquirrel()
        FS_i.pos = random_location()
        FS_i.fit = fitness_func(fitness_data, FS_i)
        var.FS.append(FS_i)

    set_best_squirrels()


def random_location():
    FS_i = []

    for j in range(var.num_of_dimensions):
        FS_ij = var.FS_l + random.uniform(0, 1) * (var.FS_u - var.FS_l)  # eq.2
        FS_i.append(FS_ij)

    return FS_i


def levy_relocation():
    FS_i = []

    for j in range(var.num_of_dimensions):
        FS_ij = var.FS_l + levy() * (var.FS_u - var.FS_l)  # eq.14
        FS_i.append(FS_ij)

    return FS_i


def levy():
    beta = 1.5  # from paper

    sigma_num = math.gamma(1+beta) * math.sin((math.pi * beta)/2)
    sigma_denom = math.gamma((1+beta)/2) * beta * 2**((beta-1)/2)
    sigma = (sigma_num / sigma_denom)**(1/beta)

    generator = get_truncated_normal()
    r_a = generator.rvs()
    r_b = generator.rvs()

    l = 0.01 * (r_a * sigma) / (math.fabs(r_b**(1/beta)))  # eq.16
    return l


# function from stackoverflow
# https://stackoverflow.com/questions/36894191/how-to-get-a-normal-distribution-within-a-range-in-numpy
def get_truncated_normal(mean=0, sd=1, low=0, upp=1):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def set_best_squirrels():
    global var
    var.FS.sort(key=lambda x: x.fit)

    var.FS_ht = var.FS[0]
    var.FS_at[0] = var.FS[1]
    var.FS_at[1] = var.FS[2]
    var.FS_at[2] = var.FS[3]


def fitness(data, FS):
    y_diff_sum = 0

    for i in range(len(data['x'])):
        y_diff_sum += math.fabs(polynomial_calc(FS.pos, data['x'][i]) - data['y'][i])

    fit = y_diff_sum  # difference between test and flying squirrels
    return fit


class FlyingSquirrel(object):
    fit = sys.maxsize
    pos = []
