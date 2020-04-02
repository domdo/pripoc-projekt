import random

num_of_dimensions = 10
num_of_agents = 50
FSl = -0.1
FSu = 0.1


def init():
    FS = []

    for i in range(num_of_agents):
        FSi = []

        for j in range(num_of_dimensions):
            FSij = FSl + random.uniform(0, 1) * (FSu - FSl)
            FSi.append(FSij)

        FS.append(FSi)
