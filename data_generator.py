import os.path
import json
import random

dir_name = "data"
filename = "data"
path = os.path.join(os.getcwd(), dir_name)

num_of_coefs = 20
num_of_x = 60

lower = -1
upper = 1


def main():
    num = 1
    file = filename + str(num) + ".json"
    file = os.path.join(path, file)
    while os.path.isfile(file):
        num += 1
        file = filename + str(num) + ".json"
        file = os.path.join(path, file)

    with open(file, 'w') as f:
        data = generate_data()
        json.dump(data, f, indent=4)


def generate_data():
    data = dict()
    data['coefs'] = []
    data['x'] = []

    for i in range(num_of_coefs):
        if random.randint(1, 10) > 1:
            c = random.uniform(lower, upper)
            c = round(c, 10)
        else:
            c = 0
            # c = None
        data['coefs'].append(c)

    x = -3.1
    for i in range(num_of_x):
        x = x + 0.1
        # x = x + random.randint(1, 5)
        data['x'].append(x)

    return data


main()