from squirrel_search import squirrel_search


def fitness(data, FS):
    fit = 0

    for x in FS.pos:
        fit += x**2

    return fit


for i in range(10):
    res = squirrel_search(fitness, num_of_agents=10, num_of_iters=1000, num_of_dims=2, FS_l=-5.12, FS_u=5.12)
    print(res.pos, res.fit)
    print()
