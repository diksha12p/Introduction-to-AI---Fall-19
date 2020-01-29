from tkinter import *
from Environment import *
from Agent import *


# Default values for dimension and number of mines
DefaultDimension = 5
DefaultNumberOfMines = 5

IS_MINE = True
IS_NOT_MINE = False
IS_VISITED = 1
IS_UNVISITED = 0
NO_CLUE = 10


class MainProgram:
    def __init__(self):
        self.env = None
        self.agent = None
        self.dimension = DefaultDimension
        self.numberOfMines = DefaultNumberOfMines
        self.window = Tk()
        self.window.title("Minesweeper Simulator")
        self.window.geometry('900x700+200+10')
        # Frame for options
        self.controlFrame = Frame(self.window, width=200, height=700)
        self.controlFrame.pack(side=LEFT)

        self.labelDim = Label(self.controlFrame, text='Dimensions')
        self.labelDim.pack()

        self.entryDim = Entry(self.controlFrame)
        self.entryDim.pack()

        self.labelNumberOfMines = Label(self.controlFrame, text='Number Of Mines')
        self.labelNumberOfMines.pack()

        self.entryNumberOfMines = Entry(self.controlFrame)
        self.entryNumberOfMines.pack()

        self.buttonGenerateMineField = Button(self.controlFrame, text="Generate MineField",
                                              command=self.generateMineField)
        self.buttonGenerateMineField.pack()

        self.buttonPlayMinesweeper = Button(self.controlFrame, text="PlayMinesweeper", command=self.playMinesweeper)
        self.buttonPlayMinesweeper.pack()
        
        self.buttonoverPlayMinesweeper = Button(self.controlFrame, text="Play Overestimated Minesweeper", command=self.playoveresMinesweeper)
        self.buttonoverPlayMinesweeper.pack()

        self.buttonPassNumber = Button(self.controlFrame, text="Pass Number of Mines and Play", command=self.playMinesweeperWithNum)
        self.buttonPassNumber.pack()

        self.buttonNextStep = Button(self.controlFrame, text="NextStep", command=self.nextStep)
        self.buttonNextStep.pack()

        # Frame for drawing minefield
        self.mineFieldFrame = Frame(self.window, width=700, height=700)
        self.mineFieldFrame.pack(side=RIGHT)

        self.mineFieldCanvas = Canvas(self.mineFieldFrame, width=700, height=700)
        self.mineFieldCanvas.pack()

        self.window.mainloop()

    def generateMineField(self):
        try:
            self.dimension = int(self.entryDim.get())
            self.numberOfMines = int(self.entryNumberOfMines.get())
        except ValueError:
            print("Invalid parameters")
            return None
        if self.numberOfMines < 0 or self.numberOfMines > (self.dimension * self.dimension):
            print("Invalid Number Of Mines, taking default value of ", DefaultNumberOfMines)
            self.numberOfMines = DefaultNumberOfMines
        self.env = Environment(self.dimension, self.numberOfMines)
        self.drawMineField(self.env.mineField)
        self.agent = Agent(self.dimension,-1)

    def drawMineField(self, mineField):
        tileHeight = (680) / self.dimension
        tileWidth = (680) / self.dimension
        self.mineFieldCanvas.delete("all")  # Clear the canvas
        tiles = [[self.mineFieldCanvas.create_rectangle(10 + i * tileWidth, 10 + j * tileHeight,
                                                        10 + (i + 1) * tileWidth, 10 + (j + 1) * tileHeight) for i in
                  range(self.dimension)] for j in range(self.dimension)]

        for i in range(self.dimension):
            for j in range(self.dimension):
                if mineField[i][j].visited == IS_UNVISITED:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#c0c0c0")
                elif mineField[i][j].visited == IS_VISITED and mineField[i][j].mine == IS_MINE:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#ff0000")
                    '''self.mineFieldCanvas.create_text(
                        (10 + tileHeight / 2 + j * tileHeight, 10 + tileWidth / 2 + i * tileWidth),
                        text=mineField[i][j].clue)
                    '''
                elif mineField[i][j].visited == IS_VISITED and mineField[i][j].mine == IS_NOT_MINE:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#ffff00")
                    self.mineFieldCanvas.create_text(
                        (10 + tileHeight / 2 + j * tileHeight, 10 + tileWidth / 2 + i * tileWidth),
                        text=mineField[i][j].clue)

    def playMinesweeper(self):
        currentBox = self.agent.selectABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes,self.agent.solvedBoxes)
            print("Query: ", currentBox.row, currentBox.col)
            queriedBox = self.env.queryBox(currentBox)
            self.agent.updateBox(queriedBox)
            currentBox = self.agent.selectABox()
        self.drawMineField(self.env.mineField)
    
    def playoveresMinesweeper(self):
        self.agent = MineSweeperOverestimatedAgent(self.dimension,-1)
        currentBox = self.agent.selectABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes,self.agent.solvedBoxes)
            print("Query: ", currentBox.row, currentBox.col)
            queriedBox = self.env.queryBox(currentBox)
            self.agent.updateBox(queriedBox)
            currentBox = self.agent.selectABox()
        self.drawMineField(self.env.mineField)

    def nextStep(self):
        currentBox = self.agent.selectABox()
        if self.agent.solvedBoxes < self.dimension ** 2:
            print("Query: ",currentBox.row,currentBox.col)
            queriedBox = self.env.queryBox(currentBox)
            self.agent.updateBox(queriedBox)
        self.drawMineField(self.env.mineField)

    def playMinesweeperWithNum(self):
        self.agent = Agent(self.dimension, self.numberOfMines)
        currentBox = self.agent.selectABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes, self.agent.solvedBoxes)
            print("Query: ", currentBox.row, currentBox.col)
            queriedBox = self.env.queryBox(currentBox)
            self.agent.updateBox(queriedBox)
            currentBox = self.agent.selectABox()
        self.drawMineField(self.env.mineField)


if __name__ == "__main__":
    mp = MainProgram()
