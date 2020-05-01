import os.path
import json
import random

dir_name = "data"
filename = "data"
path = os.path.join(os.getcwd(), dir_name)

num_of_coefs = 20
num_of_x = 60
start_x_from = -3.1

lower = -1
upper = 1


def main():
    num = 1
    file = filename + str(num) + ".json"
    file = os.path.join(path, file)
    while os.path.isfile(file): # check if file with that name exist, if yes, increase number
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

    # generate coeficients
    for i in range(num_of_coefs):
        if random.randint(1, 10) > 1:
            c = random.uniform(lower, upper)
            c = round(c, 10)
        else:  # 10% chance for coeficient to be 0
            c = 0
            # c = None
        data['coefs'].append(c)

    # generate x values
    x = start_x_from
    for i in range(num_of_x):
        x = x + 0.1
        # x = x + random.randint(1, 5)
        data['x'].append(x)

    return data


main()