# PART: Taking distance into account

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

# Flags
NOT_FOUND = False
FOUND = True


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.type = UNDECIDED_FLAG


class Agent:
    def __init__(self, env, rule, dimensions = DIMENSION_DEFAULT):
        # self.dimension = dimensions
        self.grid = [[Cell(i,j) for j in range(dimensions)] for i in range(dimensions)]
        initial_probability = float(1) / (dimensions*dimensions)
        self.belief = [[initial_probability for j in range(dimensions)] for i in range(dimensions)]
        self.env = env
        self.set_values(env)
        self.rule = rule
        self.target = NOT_FOUND
        self.dimension = dimensions
        self.number_of_steps = 0
        self.final_steps = self.solve()

    # Setting values for all the cells in the grid
    def set_values(self, env):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                self.grid[row][col].type = env.grid[row][col].type

    # Solving through the grid
    def solve(self):
        current_x_a = 0
        current_y_a = 0

        while self.target == NOT_FOUND:
            self.number_of_steps += 1
            result, row, col = self.search_target(current_x_a, current_y_a)

            current_x_a = row
            current_y_a = col

            if result:
                self.target = FOUND
                print("The true target is at {} location".format(self.env.target_cell))
                return self.number_of_steps
            else:
                self.update_belief(row,col)

    # Searching for target in the grid
    def search_target(self, current_xa, current_ya):
        max_probabilty = 0
        fringe_max_probabilty_cells = []
        # if self.rule == 1:
        #     # IDEA: Highest probability for containing the target in cell
        for a in range(self.dimension):
            for b in range(self.dimension):
                # Taking Manhattan distance into account
                distance = abs(a - current_xa) + abs(b - current_ya)
                p = self.belief[a][b] / (distance + 1)

                if p > max_probabilty:
                    max_probabilty = p
                    fringe_max_probabilty_cells = [(a,b)]
                elif p == max_probabilty:
                    fringe_max_probabilty_cells.append((a,b))
        # else:
        #         # Highest probability for finding the target in cell
        #     for a in range(self.dimension):
        #         for b in range(self.dimension):
        #             p = self.belief[a][b] * (1 - self.get_FN_score(a,b))
        #
        #             if p > max_probabilty:
        #                 max_probabilty = p
        #                 fringe_max_probabilty_cells = [(a,b)]
        #             elif p == max_probabilty:
        #                 fringe_max_probabilty_cells.append((a,b))

        search_cell = random.randint(0, len(fringe_max_probabilty_cells)-1)
        (x_a, y_a) = fringe_max_probabilty_cells[search_cell]
        return self.env.return_target(self.env.grid[x_a][y_a]), x_a, y_a
        # return_target -> Boolean Output

    # Obtaining the predefined false negative scores for the cell in the grid, contingent upon the type
    def get_FN_score(self, row, col):
        if self.grid[row][col].type == FLAT_FLAG:
            return FN_PROB_FLAT
        elif self.grid[row][col].type == HILLY_FLAG:
            return FN_PROB_HILLY
        elif self.grid[row][col].type == FOREST_FLAG:
            return FN_PROB_HILLY
        else:
            return FN_PROB_CAVE

    # Provided the target isn't found, updating the belief state using the data
    def update_belief(self, row, col):
        delta_value = (1 - self.get_FN_score(row, col)) * self.belief[row][col]
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i != row and j != col:
                    self.belief[i][j] = self.belief[i][j] / (1 - delta_value)

        self.belief[row][col] = (self.belief[row][col] - delta_value) / (1 - delta_value)
