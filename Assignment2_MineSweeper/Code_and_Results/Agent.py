import random
from sympy import symbols, S
from sympy.logic.boolalg import is_cnf, to_cnf
from sympy.logic.inference import satisfiable
import itertools

IS_MINE = True
IS_NOT_MINE = False
NO_CLUE = 10


class Box:
    def __init__(self, row, col, prob):
        self.row = row
        self.col = col
        self.clue = NO_CLUE
        self.mine = IS_NOT_MINE
        self.solved = False
        self.denotation = symbols("A" + str(row) + str(col))
        self.mineFlag = IS_NOT_MINE
        self.prob = prob

    def __str__(self):
        return "Box(" + str(self.row) + "," + str(self.col) + ")"


class Agent:

    def __init__(self, dimension, probability_input):
        self.dimension = dimension
        if probability_input == -1:
            # When no probability specified, all Boxes are equally likely
            self.agentObservedMineField = [[Box(i, j, 0.5) for j in range(self.dimension)] for i in range(self.dimension)]
        else:
            # Ensuring probability is between 0 and 1 (inclusive)
            prob = float(probability_input / dimension * dimension)
            self.agentObservedMineField = [[Box(i, j, prob) for j in range(self.dimension)] for i in range(self.dimension)]

        self.unseenBoxes = self.dimension ** 2
        self.solvedBoxes = 0
        self.knowledgeBase = S.true
        self.fringe = []
        self.numberOfMines = probability_input

    def getNeighbours(self, box):
        neighbours = []
        row, col = box.row, box.col

        for x, y in [(row + i, col + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if 0 <= x < self.dimension and 0 <= y < self.dimension:
                if not self.agentObservedMineField[x][y].mineFlag:
                    neighbours.append(self.agentObservedMineField[x][y])

        return neighbours

    def pickABox(self):
        # If the fringe isn't empty, choose a box from the fringe else, a random unsolved Box
        if len(self.fringe) != 0:
            # Choose a box from fringe
            self.fringe.sort(key=lambda x: x.prob)
            for node in self.fringe:
                if (node.prob <= 0.2):
                    # print("Row-ColSelected box", node.row, node.col)
                    return self.agentObservedMineField[node.row][node.col]

        # Choose a random unsolved box
        row = random.randrange(self.dimension)
        col = random.randrange(self.dimension)
        if self.agentObservedMineField[row][col].solved == True and self.solvedBoxes < self.dimension ** 2:
            while self.agentObservedMineField[row][col].solved:
                row = random.randrange(self.dimension)
                col = random.randrange(self.dimension)
        return self.agentObservedMineField[row][col]

    def updateBoxInfo(self, box):
        row = box.row
        col = box.col

        self.unseenBoxes -= 1
        self.solvedBoxes += 1
        if self.agentObservedMineField[row][col] in self.fringe:
            self.fringe.remove(self.agentObservedMineField[row][col])
            # print("Length Fringe:", len(self.fringe))

        self.agentObservedMineField[row][col].mine = box.mine
        self.agentObservedMineField[row][col].solved = True
        self.agentObservedMineField[row][col].clue = box.clue
        neighbours = self.getNeighbours(box)

        for neighbour in neighbours:
            if neighbour.solved == False and neighbour not in self.fringe:
                self.fringe.append(neighbour)

        self.addInfoToKnowledgeBase(self.agentObservedMineField[row][col])

    def addInfoToKnowledgeBase(self, box):
        expression_box_neighbours = S.false
        neighbours = self.getNeighbours(box)

        # CASE 1: The clue is 0 i.e. all neighbours are 'SAFE
        if box.clue == 0:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                # neighbour.solved = True
                # self.solvedBoxes += 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.denotation: False})
                if (neighbour.solved == False):
                    self.agentObservedMineField[neighbour.row][neighbour.col].prob = 0.0
                    self.fringe.append(neighbour)

        # CASE 2: 100 percent confidence in all the neighbours being a mine
        elif box.clue == 8:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    # As 'Pass by Value' is being used here
                    self.fringe.remove(neighbour)
                neighbour.solved = True
                neighbour.mineFlag = IS_MINE
                self.solvedBoxes += 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.denotation: True})
                self.agentObservedMineField[neighbour.row][neighbour.col].prob = 1.0

        # CASE 3: The clue lies between 0 and 1 (exclusive)
        else:
            for subset in itertools.combinations(neighbours, box.clue):
                expression_subset = S.true

                # Forming the expression for the neighbours of a given box
                for neighbour in neighbours:
                    if neighbour not in subset:
                        expression_subset = expression_subset & ~neighbour.denotation
                    else:
                        expression_subset = expression_subset & neighbour.denotation
                expression_box_neighbours = expression_box_neighbours | expression_subset

            # Updating the expression obtained above
            for neighbour in neighbours:
                if neighbour.solved:
                    if neighbour.mineFlag:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.denotation: True})
                    else:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.denotation: False})

            # print("Expression Generated:", expression_box_neighbours)
            expression = expression_box_neighbours

            if not is_cnf(expression):
                expression = to_cnf(expression, simplify=True)
            # print("Converted new expression")
            # print("After CNF:", expr)

            self.updateKnowledgeBaseInfo(expression, box)

    def updateKnowledgeBaseInfo(self, expression, box):
        var = box.denotation
        if box.mine == True:
            self.knowledgeBase = self.knowledgeBase.subs({var: True})
        else:
            self.knowledgeBase = self.knowledgeBase.subs({var: False})

        # Update the Knowledge Base
        self.knowledgeBase = self.knowledgeBase & expression

        if (self.knowledgeBase != S.true):
            # Keeping 'all_models' as True to obtain a generator of models
            generator_models = satisfiable(self.knowledgeBase, all_models=True)

            if len(self.fringe) != 0:
                counts = {}
                sum_mines_here = 0
                # Variable to keep a track of
                amount = 0

                # Calculate the probability
                for model in generator_models:
                    if not (isinstance(model, bool)):
                        # print model
                        try:
                            for var, value in model.items():
                                # If the value of a given item is True, increment the counter 'sum_mines_here'
                                if value == True:
                                    sum_mines_here += 1
                                    if (var in counts.keys()):
                                        counts[var] = counts[var] + 1
                                    else:
                                        counts[var] = 1
                            # Increment once the model has been dealt with
                            amount = amount + 1
                        except Exception as e:
                            print("Exception At", e)
                            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                            message = template.format(type(e).__name__, e.args)
                            print(message)

                # Calculate the fringe probabilities
                for var, value in counts.items():
                    # row, col = reverseIndex[var]
                    var = str(var)
                    row, col = int(var[1]), int(var[2])
                    if amount != 0:
                        if (float(value) / amount) >= 1:
                            print("Mine Identified for var:- ", var)
                            self.agentObservedMineField[row][col].solved = True
                            if self.agentObservedMineField[row][col] in self.fringe:
                                self.fringe.remove(self.agentObservedMineField[row][col])
                            self.unseenBoxes -= 1
                            self.solvedBoxes += 1
                            self.agentObservedMineField[row][col].mineFlag = IS_MINE
                            var = self.agentObservedMineField[row][col].denotation
                            self.knowledgeBase = self.knowledgeBase.subs({var: True})
                            self.knowledgeBase = self.knowledgeBase & S.true
                            self.agentObservedMineField[row][col].prob = 1
                        else:
                            if (self.agentObservedMineField[row][col] in self.fringe):
                                self.agentObservedMineField[row][col].prob += float(value) / amount
                            else:
                                self.agentObservedMineField[row][col].prob = float(value) / amount

                if amount != 0:
                    prob = float((self.numberOfMines - self.solvedBoxes) * amount - sum_mines_here) / (
                            amount * self.unseenBoxes)
                    for row in range(self.dimension):
                        for col in range(self.dimension):
                            if self.agentObservedMineField[row][col].solved == False and self.agentObservedMineField[row][col] not in self.fringe:
                                self.agentObservedMineField[row][col].prob = prob


class MineSweeperOverestimatedAgent(Agent):

    def __init__(self, dimention, probability_input):
        super(MineSweeperOverestimatedAgent, self).__init__(dimention, probability_input)

    def addInfoToKnowledgeBase(self, box):
        expression_box_neighbours = S.false
        neighbours = self.getNeighbours(box)
        if box.clue == 0:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                # neighbour.solved = True
                # self.solvedBoxes += 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.denotation: False})
                if (neighbour.solved == False):
                    self.agentObservedMineField[neighbour.row][neighbour.col].prob = 0.0
                    self.fringe.append(neighbour)
        elif box.clue == 8:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                neighbour.solved = True
                neighbour.mineFlag = IS_MINE
                self.solvedBoxes += 1
                # self.unseenBoxes -= 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.denotation: True})
                self.agentObservedMineField[neighbour.row][neighbour.col].prob = 1.0

        else:
            for clue_i in range(0, box.clue + 1):
                for subset in itertools.combinations(neighbours, box.clue):
                    expression_subset = S.true

                    for neighbour in neighbours:
                        if neighbour not in subset:
                            expression_subset = expression_subset & ~neighbour.denotation
                        else:
                            expression_subset = expression_subset & neighbour.denotation
                    expression_box_neighbours = expression_box_neighbours | (expression_subset)
            for neighbour in neighbours:
                if neighbour.solved:
                    if neighbour.mineFlag:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.denotation: True})
                    else:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.denotation: False})

            expression = expression_box_neighbours

            if not is_cnf(expression):
                expression = to_cnf(expression, simplify=True)

            self.updateKnowledgeBaseInfo(expression, box)
