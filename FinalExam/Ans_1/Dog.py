# Game Over -1
import random
import numpy as np

dim = 8
diag_elem_1 = (3, 4)
diag_elem_2 = (4, 3)


class Dog:

    def get_neighbors(self, row, col, env, dim=8):
        neighbors = []

        sheep = env.sheep_location()
        dogs = env.dog_location()

        for x, y in [(row + i, col + j) for j in (-1, 0, 1) for i in (-1, 0, 1)]:
            if abs(x - row) + abs(y - col) == 1:
                if (0 <= x < dim) and (0 <= y < dim):
                    if env.grid[x][y] == 0:
                        neighbors.append([x, y])

        return neighbors


    def manhattan_dist(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def move_to_dest(self, currentloc, dest, env):
        if not (currentloc[0] == dest[0] and currentloc[1] == dest[1]):

            neighbors = self.get_neighbors(currentloc[0], currentloc[1], env)
            print(neighbors)
            distances = []
            for n in neighbors:
                distances.append(self.manhattan_dist(n, dest))
            index = np.argmin(distances)
            # neighbors[index]
            if env.rowDog1 == currentloc[0] and env.colDog1 == currentloc[1]:
                env.update_dog_location(neighbors[index][0], neighbors[index][1], env.rowDog2, env.colDog2)
            else:
                env.update_dog_location(env.rowDog1, env.colDog1, neighbors[index][0], neighbors[index][1])
        else:
            print("Do nothing")

    def get_diagonal_for_dogs(self, env):
        dogs = env.dog_location()
        dog1 = [dogs[0], dogs[1]]
        # dog1_dist2 = [dogs[2], dogs[3]]
        dog1_dist1 = self.manhattan_dist(dog1, diag_elem_1)
        dog1_dist2 = self.manhattan_dist(dog1, diag_elem_2)
        if dog1_dist1 > dog1_dist2:
            dog1_destination = diag_elem_2
            dog2_destination = diag_elem_1
        else:
            dog1_destination = diag_elem_1
            dog2_destination = diag_elem_2

        return dog1_destination, dog2_destination

    def move_dogs_jointly(self, env):
        neighbors1 = self.get_neighbors(env.rowDog1, env.colDog1, env)
        neighbors2 = self.get_neighbors(env.rowDog2, env.colDog2, env)
        distances = []
        for n1 in neighbors1:
            distances.append(self.manhattan_dist(n1, [env.rowSheep, env.colSheep]))
        index = np.argmin(distances)
        deltar = neighbors1[index][0] - env.rowDog1
        deltac = neighbors1[index][1] - env.colDog1
        if env.rowDog2 + deltar < dim and env.rowDog2 + deltar >= 0 and env.colDog2 + deltac < dim and env.colDog2 + deltac >= 0 and (env.grid[env.rowDog2 + deltar][env.colDog2 + deltac] == 0):
            env.update_dog_location(neighbors1[index][0], neighbors1[index][1], env.rowDog2 + deltar,
                                    env.colDog2 + deltac)
