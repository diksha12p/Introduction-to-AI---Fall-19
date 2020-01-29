# Game over -1
import random

dim = 8


class Sheep:

    def get_neighbors(self, row, col, env, dim=8):
        neighbors = []

        dogs = env.dog_location()
        for x, y in [(row + i, col + j) for j in (-1, 0, 1) for i in (-1, 0, 1)]:

            if abs(x - row) + abs(y - col) == 1:

                if (0 <= x < dim) and (0 <= y < dim):
                    # print("Here")
                    # print(x, row, y, col)
                    # if (not (x == dogs[0] and y == dogs[1]) and not (
                    #         x == dogs[2] and y == dogs[3])):  # check if logically correct
                    if env.grid[x][y]==0:
                        neighbors.append([x, y])

        return neighbors

    def move(self, env):
        curr_row = env.rowSheep
        curr_col = env.colSheep
        neighbors = self.get_neighbors(curr_row, curr_col, env)
        if len(neighbors) == 0 and curr_row == 0 and curr_col == 0:
            return -1
        # print(neighbors)
        if len(neighbors) >= 1:
            index = random.randrange(0, len(neighbors))
            env.update_sheep_location(neighbors[index][0], neighbors[index][1])
            # print("Sheep CHANGES location to ({},{})".format(neighbors[index][0], neighbors[index][1]))
        else:
            print()
            # env.update_sheep_location(curr_row, curr_col)
            # print("Sheep RETAINS location ({},{})".format(curr_row, curr_col))
