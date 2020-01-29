import math
import operator
import os


def eucledian_distance(list_1, list_2):
    euc_distance = 0
    for curr_point in range(len(list_1)):
        euc_distance += pow((list_1[curr_point] - list_2[curr_point]), 2)
    return math.sqrt(euc_distance)


def fetch_neighbours(train_data, gen_data, k):
    dist_result, neighbours_list = [], []
    for i in range(len(train_data)):
        dist_data = eucledian_distance(train_data[i], gen_data)
        dist_result.append((i, dist_data))
    dist_result.sort(key=operator.itemgetter(1))
    for i in range(k):
        neighbours_list.append(dist_result[i][0])
    return neighbours_list


def fetch_results(neighbours):
    classA, classB = 0, 0
    for n in neighbours:
        if output[n] == 0:
            classA += 1
        else:
            classB += 1
    if classA > classB:
        print("Belongs to Class A")
    else:
        print("Belongs to Class B")


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


if __name__ == '__main__':
    image_type_A = gen_list('ClassA')
    image_type_B = gen_list('ClassB')
    train_data = image_type_A + image_type_B
    output = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

    print("= = = = = = = = \nTraining Data \n= = = = = = = = ")
    for curr_train_data in train_data:
        neighbours = fetch_neighbours(train_data, curr_train_data, k=3)
        fetch_results(neighbours)

    image_type_Mystery = gen_list('Mystery')
    print("= = = = = = = = \nTesting Data \n= = = = = = = = ")
    for curr_test_data in image_type_Mystery:
        neighbours = fetch_neighbours(train_data, curr_test_data, k=3)
        fetch_results(neighbours)
