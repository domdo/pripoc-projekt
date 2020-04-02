import os.path
import json

dir_name = "data"
path = os.path.join(os.getcwd(), dir_name)


def main():
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        with open(file, 'r+') as f:
            data = json.load(f)
            data['y'] = []

            for x in data['x']:
                data['y'].append(polynomial_calc(data['coefs'], x))

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


def polynomial_calc(coefs, x):
    n = 0
    y = 0
    for c in coefs:
        if isinstance(c, float):
            y = y + (c * (x**n))
        n += 1
    y = round(y, 2)
    return y


main()