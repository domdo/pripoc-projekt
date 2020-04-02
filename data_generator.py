import os.path
import json
import random

dir_name = "data"
filename = "data"
path = os.path.join(os.getcwd(), dir_name)

num_of_coefs = 10
num_of_x = 50


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
        if random.randint(1, 10) > 2:
            c = random.uniform(-0.0000001, 0.0000001)
            c = round(c, 10)
        else:
            c = None
        data['coefs'].append(c)

    x = 0
    for i in range(num_of_x):
        x = x + random.randint(1, 5)
        data['x'].append(x)

    return data


main()