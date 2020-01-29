# Initial location of the dogs and sheep is set

# Sheep =1
# Dog=2
# dim=8
import random


class Environment:
    def __init__(self, dim=8):
        self.grid = [[0] * dim for j in range(dim)]
        self.rowSheep = 4
        self.colSheep = 0
        self.grid[self.rowSheep][self.colSheep] = 1  # Sheep

        self.rowDog1 = 6
        self.colDog1 = 3

        self.grid[self.rowDog1][self.colDog1] = 2   # Dog1

        self.rowDog2 = 0
        self.colDog2 = 7
        self.grid[self.rowDog2][self.colDog2] = 2   # Dog2

    def sheep_location(self):
        return [self.rowSheep, self.colSheep]

    def dog_location(self):
        return [self.rowDog1, self.colDog1, self.rowDog2, self.colDog2]

    def update_sheep_location(self, row, col):
        self.grid[self.rowSheep][self.colSheep] = 0
        self.rowSheep = row
        self.colSheep = col
        self.grid[self.rowSheep][self.colSheep] = 1
        print("Sheep moved to{}, {}".format(self.rowSheep, self.colSheep))

    def update_dog_location(self, row1, col1, row2, col2):
        self.grid[self.rowDog1][self.colDog1] = 0
        self.grid[self.rowDog2][self.colDog2] = 0
        self.rowDog1 = row1
        self.colDog1 = col1
        self.rowDog2 = row2
        self.colDog2 = col2
        self.grid[self.rowDog1][self.colDog1] = 2
        self.grid[self.rowDog2][self.colDog2] = 2
        print("Dog 1 moved to{}, {}".format(self.rowDog1, self.colDog1))
        print("Dog 2 moved to{}, {}".format(self.rowDog2, self.colDog2))

    # def move_left(self,row,col):


    def find_sheep_quadrant(self):
        if self.rowSheep <= 3 and self.colSheep <= 3:
            return 1
        elif self.rowSheep <= 3 and self.colSheep > 3:
            return 2
        elif self.rowSheep > 3 and self.colSheep <= 3:
            return 3
        else:
            return 4
