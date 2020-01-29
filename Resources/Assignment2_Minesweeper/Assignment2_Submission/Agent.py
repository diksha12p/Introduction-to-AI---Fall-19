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
        self.symbol = symbols("A" + str(row) + str(col))
        self.mineFlag = IS_NOT_MINE
        self.prob = prob

    def __str__(self):
        return "Box(" + str(self.row) + "," + str(self.col) + ")"


class Agent:

    def __init__(self, dimension, number):
        self.dimension = dimension
        if number == -1:
            self.observedMineField = [[Box(i, j, 0.5) for j in range(self.dimension)] for i in range(self.dimension)]
        else:
            prob = float(number / dimension * dimension)
            self.observedMineField = [[Box(i, j, prob) for j in range(self.dimension)] for i in range(self.dimension)]
        self.unseenBoxes = self.dimension * self.dimension
        self.solvedBoxes = 0
        self.knowledgeBase = S.true
        self.fringe = []
        self.numberOfMines = number

    def getNeighbours(self, box):
        neighbours = []
        row, col = box.row, box.col

        for x, y in [(row + i, col + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if x >= 0 and x < self.dimension and y >= 0 and y < self.dimension:
                if self.observedMineField[x][y].mineFlag == False:
                    neighbours.append(self.observedMineField[x][y])

        return neighbours

    def selectABox(self):
        minProbCells = []
        if len(self.fringe) != 0:
            # Choose a box from fringe

            self.fringe.sort(key=lambda x: x.prob)
            for node in self.fringe:
                if (node.prob <= 0.2):
                    # print("Row-ColSelected box", node.row, node.col)
                    return self.observedMineField[node.row][node.col]

        # Choose a random unsolved box
        row = random.randrange(self.dimension)
        col = random.randrange(self.dimension)
        if self.observedMineField[row][col].solved == True and self.solvedBoxes < self.dimension ** 2:
            while self.observedMineField[row][col].solved == True:
                row = random.randrange(self.dimension)
                col = random.randrange(self.dimension)
        # print("Row-ColSelected box", row, col)
        return self.observedMineField[row][col]

    def updateBox(self, box):
        row = box.row
        col = box.col

        self.unseenBoxes -= 1
        self.solvedBoxes += 1
        if self.observedMineField[row][col] in self.fringe:
            self.fringe.remove(self.observedMineField[row][col])
            # print("Length Fringe:", len(self.fringe))

        self.observedMineField[row][col].mine = box.mine
        self.observedMineField[row][col].solved = True
        self.observedMineField[row][col].clue = box.clue
        neighbours = self.getNeighbours(box)
        for neighbour in neighbours:
            if neighbour.solved == False and neighbour not in self.fringe:
                self.fringe.append(neighbour)

        self.addToKnowledgeBase(self.observedMineField[row][col])

    def addToKnowledgeBase(self, box):
        expression_box_neighbours = S.false
        neighbours = self.getNeighbours(box)
        if box.clue == 0:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                # neighbour.solved = True
                # self.solvedBoxes += 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.symbol: False})
                if (neighbour.solved == False):
                    self.observedMineField[neighbour.row][neighbour.col].prob = 0.0
                    self.fringe.append(neighbour)
        elif box.clue == 8:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                neighbour.solved = True
                neighbour.mineFlag = IS_MINE
                self.solvedBoxes += 1
                # self.unseenBoxes -= 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.symbol: True})
                self.observedMineField[neighbour.row][neighbour.col].prob = 1.0

        else:
            for subset in itertools.combinations(neighbours, box.clue):
                expression_subset = S.true

                for neighbour in neighbours:
                    if neighbour not in subset:
                        expression_subset = expression_subset & ~neighbour.symbol
                    else:
                        expression_subset = expression_subset & neighbour.symbol
                expression_box_neighbours = expression_box_neighbours | (expression_subset)
            for neighbour in neighbours:
                if neighbour.solved == True:
                    if neighbour.mineFlag:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.symbol: True})
                    else:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.symbol: False})

            # print("Expression Generated:", expression_box_neighbours)
            expr = expression_box_neighbours

            if not is_cnf(expr):
                expr = to_cnf(expr, simplify=True)
            # print("Converted new expression")
            # print("After CNF:", expr)

            self.updateKnowledgeBase(expr, box)

    def updateKnowledgeBase(self, expression, box):
        var = box.symbol
        if box.mine == True:
            # self.numberOfMines -= 1
            self.knowledgeBase = self.knowledgeBase.subs({var: True})
        else:
            self.knowledgeBase = self.knowledgeBase.subs({var: False})

        self.knowledgeBase = self.knowledgeBase & expression
        # self.knowledgeBase = simplify_logic(self.knowledgeBase, form="cnf")
        # print("KB:", self.knowledgeBase)

        if (self.knowledgeBase != S.true):
            assignments = satisfiable(self.knowledgeBase, all_models=True)

            if len(self.fringe) != 0:
                counts = {}
                totalMinesHere = 0
                amount = 0
                # Calculate probability
                for model in assignments:
                    if not (isinstance(model, bool)):
                        # print model
                        try:
                            for var, value in model.items():
                                if value == True:
                                    totalMinesHere += 1
                                    if (var in counts.keys()):
                                        counts[var] = counts[var] + 1
                                    else:
                                        counts[var] = 1
                            amount = amount + 1
                        except Exception as e:
                            print("Exception at", e)
                            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                            message = template.format(type(e).__name__, e.args)
                            print(message)
                # The probability for fringe cells
                for var, value in counts.items():
                    # row, col = reverseIndex[var]
                    var = str(var)
                    row, col = int(var[1]), int(var[2])
                    if amount != 0:
                        if (float(value) / amount) >= 1:
                            print("Mine Identified for var:- ", var)
                            self.observedMineField[row][col].solved = True
                            if self.observedMineField[row][col] in self.fringe:
                                self.fringe.remove(self.observedMineField[row][col])
                            self.unseenBoxes -= 1
                            self.solvedBoxes += 1
                            self.observedMineField[row][col].mineFlag = IS_MINE
                            var = self.observedMineField[row][col].symbol
                            self.knowledgeBase = self.knowledgeBase.subs({var: True})
                            self.knowledgeBase = self.knowledgeBase & S.true
                            self.observedMineField[row][col].prob = 1
                        else:
                            if (self.observedMineField[row][col] in self.fringe):
                                self.observedMineField[row][col].prob += float(value) / amount
                            else:
                                self.observedMineField[row][col].prob = float(value) / amount
                            # print("Prob of postion -", row, col, float(value) / amount)

                # if (self.numberOfMines > -1):
                if (amount != 0):
                    prob = float((self.numberOfMines - self.solvedBoxes) * amount - totalMinesHere) / (
                            amount * self.unseenBoxes)
                    for row in range(self.dimension):
                        for col in range(self.dimension):
                            if self.observedMineField[row][col].solved == False and self.observedMineField[row][
                                col] not in self.fringe:
                                self.observedMineField[row][col].prob = prob


class MineSweeperOverestimatedAgent(Agent):

    def __init__(self, dimention, number):
        super(MineSweeperOverestimatedAgent, self).__init__(dimention, number)

    def addToKnowledgeBase(self, box):
        expression_box_neighbours = S.false
        neighbours = self.getNeighbours(box)
        if box.clue == 0:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                # neighbour.solved = True
                # self.solvedBoxes += 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.symbol: False})
                if (neighbour.solved == False):
                    self.observedMineField[neighbour.row][neighbour.col].prob = 0.0
                    self.fringe.append(neighbour)
        elif box.clue == 8:
            for neighbour in neighbours:
                if neighbour in self.fringe:
                    self.fringe.remove(neighbour)
                neighbour.solved = True
                neighbour.mineFlag = IS_MINE
                self.solvedBoxes += 1
                # self.unseenBoxes -= 1
                self.knowledgeBase = self.knowledgeBase.subs({neighbour.symbol: True})
                self.observedMineField[neighbour.row][neighbour.col].prob = 1.0

        else:
            for ci in range(0, box.clue + 1):
                for subset in itertools.combinations(neighbours, box.clue):
                    expression_subset = S.true

                    for neighbour in neighbours:
                        if neighbour not in subset:
                            expression_subset = expression_subset & ~neighbour.symbol
                        else:
                            expression_subset = expression_subset & neighbour.symbol
                    expression_box_neighbours = expression_box_neighbours | (expression_subset)
            for neighbour in neighbours:
                if neighbour.solved == True:
                    if neighbour.mineFlag:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.symbol: True})
                    else:
                        expression_box_neighbours = expression_box_neighbours.subs({neighbour.symbol: False})

            # print("Expression Generated:", expression_box_neighbours)
            expr = expression_box_neighbours

            if not is_cnf(expr):
                expr = to_cnf(expr, simplify=True)
            # print("Converted new expression")
            # print("After CNF:", expr)

            self.updateKnowledgeBase(expr, box)
