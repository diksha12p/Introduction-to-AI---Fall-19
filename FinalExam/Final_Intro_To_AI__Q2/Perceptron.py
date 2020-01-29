import numpy as np
import os
import math


class Classifier:
    def __init__(self, X, y, learning_rate=0.01, max_iter=1000):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.weights = np.zeros(X.shape[1])
        self.output = []
        self.X = X
        self.y = y
        self.bias = 0

    def func_sigmoid_activation(self, x):
        # return 1.0 / (1 + np.exp(-x))
        return 1.0 / (1 + np.exp(-x))

    def derivative_sigmoid_activation(self, x):
        # Sigmoid derivative : sigma(x) * (1 - sigma(x))
        return self.func_sigmoid_activation(x) * (1 - self.func_sigmoid_activation(x))

    def train(self):
        for i in range(self.max_iter):
            self.output = []
            for x_i in self.X:
                self.output.append(self.func_sigmoid_activation(np.dot(x_i, self.weights) + self.bias))

            for x_i, target, op in zip(self.X, self.y, self.output):
                update = self.learning_rate * (target - op) * self.func_sigmoid_activation(op)
                new_weights = np.dot(x_i.T, update)
                self.weights += new_weights
                self.bias += update

    def test(self, X):
        self.output = []
        for x_i in X:
            self.output.append(self.func_sigmoid_activation(np.dot(x_i, self.weights) + self.bias))
        print("= = = = = = = = \nValues for the grids:\n= = = = = = = =")
        print("Grid 1 : {}".format(self.output[0]))
        print("Grid 2 : {}".format(self.output[1]))
        print("Grid 3 : {}".format(self.output[2]))
        print("Grid 4 : {}".format(self.output[3]))
        print("Grid 5 : {}".format(self.output[4]))

        return self.output


def gen_list(my_file):
        path = './'

        for filename in os.listdir(path):
            if filename == '{}.txt'.format(my_file):

                with open(filename, 'r') as f:
                    lines = f.readlines()

                img, temp = [], []
                for line in lines:
                    if line != "\t\t\t\t\n":
                        line = line.strip("\n")
                        temp.extend(line.split("\t"))

                    else:
                        img.append(list(map(int, temp)))
                        temp = []
                img.append(list(map(int, temp)))
                return img


image_type_A = gen_list('ClassA')
image_type_B = gen_list('ClassB')
train_data = image_type_A + image_type_B
output = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

X = np.array(train_data)
y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

cs = Classifier(X, y)
cs.train()
output = cs.test(X)
print("Training Error")
# print("= = = = = = = = \nTraining Data \n= = = = = = = = ")
for o in output:
    if o > 0.5:
        print("Belongs to Class B")
    else:
        print("Belongs to Class A")

image_type_Mystery = gen_list('Mystery')

X = np.array(image_type_Mystery)
output = cs.test(X)
print("= = = = = = = = \nTesting Data \n= = = = = = = = ")
for o in output:
    if o > 0.5:
        print("Belongs to Class B")
    else:
        print("Belongs to Class A")
