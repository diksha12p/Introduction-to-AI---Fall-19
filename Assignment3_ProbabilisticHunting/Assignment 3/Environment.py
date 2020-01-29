import random

# Variables
DIMENSION_DEFAULT = 50
UNDECIDED_FLAG = 0
FLAT_FLAG = 1
HILLY_FLAG = 2
FOREST_FLAG = 3
CAVE_FLAG = 4

# Probability of FALSE NEGATIVES
FN_PROB_FLAT = 0.1
FN_PROB_HILLY = 0.3
FN_PROB_FOREST = 0.7
FN_PROB_CAVE = 0.9

# Other Flags
TARGET_FLAG = True
NOT_TARGET_FLAG = False


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.type = UNDECIDED_FLAG
        self.target = NOT_TARGET_FLAG
        # self.target_cell = None


class Environment:
    def __init__(self, dimensions):
        self.grid = [[Cell(i, j) for j in range(dimensions)] for i in range(dimensions)]
        self.target_cell = None
        self.set_values()

    def set_values(self):
        total_cells = len(self.grid) * len(self.grid)

        flat_cells = 0.2 * total_cells
        hilly_cells = 0.3 * total_cells
        forest_cells = 0.2 * total_cells
        # The rest cells will be automatically assigned to 'cave' type

        for i in range(total_cells):
            # Assigning each cell a type of terrain
            row = random.randrange(len(self.grid))
            col = random.randrange(len(self.grid))
            while self.grid[row][col].type != UNDECIDED_FLAG:
                row = random.randrange(len(self.grid))
                col = random.randrange(len(self.grid))

            if i < flat_cells:
                self.grid[row][col].type = FLAT_FLAG
            elif i < flat_cells + hilly_cells:
                self.grid[row][col].type = HILLY_FLAG
            elif i < flat_cells + hilly_cells + forest_cells:
                self.grid[row][col].type = FOREST_FLAG
            else:
                self.grid[row][col].type = CAVE_FLAG

        # Setting up target value
        row = random.randrange(len(self.grid))
        col = random.randrange(len(self.grid))
        self.grid[row][col].target = TARGET_FLAG
        print("Target is at : ({0} , {1})".format(row, col))
        self.target_cell = (row, col)

    # Ensuring that the method is executed only once
    @staticmethod
    def return_target(cell):
        if cell.target == NOT_TARGET_FLAG:
            return False
        else:
            rand = random.random()
            if cell.type == FLAT_FLAG and rand > FN_PROB_FLAT:
                return True
            elif cell.type == HILLY_FLAG and rand > FN_PROB_HILLY:
                return True
            elif cell.type == FOREST_FLAG and rand > FN_PROB_FOREST:
                return True
            elif cell.type == CAVE_FLAG and rand > FN_PROB_CAVE:
                return True
            else:
                return False





