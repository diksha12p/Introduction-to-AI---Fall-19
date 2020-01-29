import random

DefaultDimension = 5
DefaultNumberOfMines = 5


IS_MINE = True
IS_NOT_MINE = False
IS_UNVISITED = 0
IS_VISITED = 1
NO_CLUE = 10


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mine = IS_NOT_MINE
        self.visited = IS_UNVISITED
        self.clue = NO_CLUE



class Environment:

    def __init__(self, dimension, numberOfMines):
        self.mineField = [[Cell(i, j) for j in range(dimension)] for i in range(dimension)]
        self.generateMineFieldValues(dimension, numberOfMines)
        self.generateInformation()

    def generateMineFieldValues(self, dimension, numberOfMines):
        # Generation of mines
        for i in range(numberOfMines):
            row = random.randrange(dimension)
            col = random.randrange(dimension)

            while self.mineField[row][col].mine != IS_NOT_MINE:
                row = random.randrange(dimension)
                col = random.randrange(dimension)
            self.mineField[row][col].mine = IS_MINE

        print(self.mineField)

    def generateInformation(self):
        dim = len(self.mineField)
        for row in range(dim):
            for col in range(dim):
                count = 0
                for x, y in [(row + i, col + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
                    if (x >= 0 and x < dim) and (y >= 0 and y < dim):
                        if self.mineField[x][y].mine == IS_MINE:
                            count += 1
                self.mineField[row][col].clue = count
        print([[(i, j, self.mineField[i][j].clue) for j in range(dim)] for i in range(dim)])
        print([[(i, j, self.mineField[i][j].mine) for j in range(dim)] for i in range(dim)])

    def queryBox(self, box):
        row = box.row
        col = box.col
        self.mineField[row][col].visited = IS_VISITED
        return self.mineField[row][col]
