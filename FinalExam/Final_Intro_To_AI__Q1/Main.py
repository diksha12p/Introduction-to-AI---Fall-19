from Environment import Environment
from Sheep import Sheep
from Dog import Dog
import statistics
import numpy as np


if __name__ == '__main__':
    count_values = []
    for curr_ptr in range(100):

        count = 0
        env = Environment()
        sheep = Sheep()
        dogs = Dog()
        print("Sheep location {} {}".format(env.rowSheep, env.colSheep))
        print("Dog1 location {} {}".format(env.rowDog1, env.colDog1))
        print("Dog2 location {} {}".format(env.rowDog2, env.colDog2))

        diag1, diag2 = dogs.get_diagonal_for_dogs(env)
        while not (diag1[0] == env.rowDog1 and diag1[1] == env.colDog1 and diag2[0] == env.rowDog2 and diag2[
            1] == env.colDog2):
            dogs.move_to_dest([env.rowDog1, env.colDog1], diag1, env)
            dogs.move_to_dest([env.rowDog2, env.colDog2], diag2, env)

            sheep.move(env)
            count += 1
        print("---------------------------------------Dogs are at the diagonal")


        while dogs.manhattan_dist([env.rowSheep, env.colSheep], [env.rowDog1, env.colDog1]) > 0:

            # Corner 00
            if (env.grid[0][0] == 1 and env.grid[1][0] == 2 and env.grid[0][1] == 2):
                print("Sheep Cornered in steps: \t", count)
                count_values.append(count)
                break
            # Corner 007
            if (env.grid[0][7] == 1 and env.grid[1][7] == 2 and env.grid[0][6] == 2):
                print("Sheep Cornered at 07 \t", count)
                dogs.move_to_dest([0, 6], [1, 6], env)
                sheep.move(env)
                count += 1
                dogs.move_to_dest([1, 7], [0, 7], env)
                sheep.move(env)
                count += 1

            # Corner 70
            if (env.grid[7][0] == 1 and env.grid[7][1] == 2 and env.grid[6][0] == 2):
                print("Sheep Cornered at 70 \t", count)
                dogs.move_to_dest([6, 0], [6, 1], env)
                sheep.move(env)
                count += 1
                dogs.move_to_dest([7, 1], [7, 0], env)
                sheep.move(env)
                count += 1

            # Corner 77
            if (env.grid[7][7] == 1 and env.grid[7][6] == 2 and env.grid[6][7] == 2):
                print("Sheep Cornered at 77 \t", count)
                dogs.move_to_dest([7, 6], [6, 6], env)
                sheep.move(env)
                count += 1
                dogs.move_to_dest([6, 7], [7, 7], env)
                sheep.move(env)
                count += 1

            if dogs.manhattan_dist([env.rowSheep, env.colSheep], [env.rowDog1, env.colDog1]) != dogs.manhattan_dist(
                    [env.rowSheep, env.colSheep], [env.rowDog2, env.colDog2]):
                [row1, col1] = [env.rowDog1, env.colDog1]
                [row2, col2] = [env.rowDog2, env.colDog2]
                dogs.move_to_dest([env.rowDog1, env.colDog1], [row1, col2], env)
                dogs.move_to_dest([env.rowDog2, env.colDog2], [row2, col1], env)

                sheep.move(env)
                count += 1

            dogs.move_dogs_jointly(env)
            sheep.move(env)
            count += 1
            print("---------")


    print("Mode {}".format(statistics.mode(count_values)))
