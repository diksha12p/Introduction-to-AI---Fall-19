from tkinter import *
from Environment import *
from Agent import *
import datetime


# Default values for dimension and number of mines
dimension_default = 5
numberOfMines_default = 5

IS_MINE = True
IS_NOT_MINE = False
IS_VISITED = 1
IS_UNVISITED = 0
NO_CLUE = 10

# root = Tk()
#
# lab = Label(root)
# lab.pack()

#
# def clock():
#     time = datetime.datetime.now().strftime("Time: %H:%M:%S")
#     lab.config(text=time)
#     # lab['text'] = time
#     root.after(1000, clock)  # run itself again after 1000 ms


class MainProgram:
    def __init__(self):
        self.environment = None
        self.agent = None
        self.dimension = dimension_default
        self.numberOfMines = numberOfMines_default

        # Tkinter Window specifications
        self.window = Tk()
        self.window.title("Minesweeper Simulator")
        self.window.geometry('1200x1200+100+10')

        # Frame for options
        self.controlFrame = Frame(self.window, width=200, height=700)
        self.controlFrame.pack(side=LEFT)

        self.DimensionLabel = Label(self.controlFrame, text='Enter Dimension')
        self.DimensionLabel.pack()

        self.DimensionEntry = Entry(self.controlFrame)
        self.DimensionEntry.pack()

        self.NumberOfMinesLabel = Label(self.controlFrame, text='Enter Number Of Mines')
        self.NumberOfMinesLabel.pack()

        self.NumberOfMinesEntry = Entry(self.controlFrame)
        self.NumberOfMinesEntry.pack()

        self.GenerateMineFieldButton = Button(self.controlFrame, text="Generate the MineField",
                                              command=self.mineFieldGeneration)
        self.GenerateMineFieldButton.pack()

        self.PlayMinesweeperButton = Button(self.controlFrame, text="Auto-Play Minesweeper", command=self.autoPlayMinesweeper)
        self.PlayMinesweeperButton.pack()

        self.OverEstPlayMinesweeperButton = Button(self.controlFrame, text="Auto-Play Overestimated Minesweeper", command=self.autoPlayOverEstMinesweeper)
        self.OverEstPlayMinesweeperButton.pack()

        self.PassNumberButton = Button(self.controlFrame, text="Pass Number of Mines and Play", command=self.playMinesweeperGivenNumber)
        self.PassNumberButton.pack()

        self.NextStepButton = Button(self.controlFrame, text="Next Step", command=self.nextStep)
        self.NextStepButton.pack()

        # Frame for drawing minefield
        self.mineFieldFrame = Frame(self.window, width=700, height=700)
        self.mineFieldFrame.pack(side=RIGHT)

        self.mineFieldCanvas = Canvas(self.mineFieldFrame, width=700, height=700)
        self.mineFieldCanvas.pack()

        self.window.mainloop()

    # Function for generating the Mine Field according to dimension and number of mines passed by the user
    def mineFieldGeneration(self):
        try:
            self.dimension = int(self.DimensionEntry.get())
            self.numberOfMines = int(self.NumberOfMinesEntry.get())
        except ValueError:
            print("Invalid Parameters Entered !!")
            return None
        # Checking the validity of the entered value for 'numberOfMines'. If invalid, its set to default
        if self.numberOfMines < 0 or self.numberOfMines > (self.dimension ** 2):
            print("Invalid Number Of Mines, assigning default value : ", numberOfMines_default)
            self.numberOfMines = numberOfMines_default
        self.environment = Environment(self.dimension, self.numberOfMines)
        self.mineFieldSketch(self.environment.mineField)
        self.agent = Agent(self.dimension,-1)

    # Function to sketch out the mine field to the user
    def mineFieldSketch(self, mineField):
        tileHeight = (680) / self.dimension
        tileWidth = (680) / self.dimension
        # Clear the canvas
        self.mineFieldCanvas.delete("all")
        tiles = [[self.mineFieldCanvas.create_rectangle(10 + i * tileWidth, 10 + j * tileHeight,
                                                        10 + (i + 1) * tileWidth, 10 + (j + 1) * tileHeight) for i in
                  range(self.dimension)] for j in range(self.dimension)]

        # Assigning corresponding colours to the rectangles (RED if mine, GREEN if visited and GRAY if unvisited)
        for i in range(self.dimension):
            for j in range(self.dimension):
                if mineField[i][j].visited == IS_UNVISITED:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#a19999") #GRAY
                elif mineField[i][j].visited == IS_VISITED and mineField[i][j].mine == IS_MINE:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#c70a0a") #RED
                elif mineField[i][j].visited == IS_VISITED and mineField[i][j].mine == IS_NOT_MINE:
                    self.mineFieldCanvas.itemconfig(tiles[i][j], fill="#116b58") #GREEN
                    # If visited and not a mine, the corresponding clue is written in the rectangle
                    self.mineFieldCanvas.create_text(
                        (10 + tileHeight / 2 + j * tileHeight, 10 + tileWidth / 2 + i * tileWidth),
                        text=mineField[i][j].clue)

    #Function to initiate continuous play of minesweeper
    def autoPlayMinesweeper(self):
        current_box = self.agent.pickABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes,self.agent.solvedBoxes)
            # Printing to the user the current box being queried
            print("Query: ", current_box.row, current_box.col)
            queried_box = self.environment.QueryMethodBox(current_box)
            self.agent.updateBoxInfo(queried_box)
            current_box = self.agent.pickABox()
        self.mineFieldSketch(self.environment.mineField)

    #Function to initiate continuous play of the overestimated version of minesweeper
    def autoPlayOverEstMinesweeper(self):
        self.agent = MineSweeperOverestimatedAgent(self.dimension,-1)
        current_box = self.agent.pickABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes,self.agent.solvedBoxes)
            print("Query: ", current_box.row, current_box.col)
            queried_box = self.environment.QueryMethodBox(current_box)
            self.agent.updateBoxInfo(queried_box)
            current_box = self.agent.pickABox()
        self.mineFieldSketch(self.environment.mineField)

    # Function to just play the next step of the game
    def nextStep(self):
        current_box = self.agent.pickABox()
        if self.agent.solvedBoxes < self.dimension ** 2:
            print("Query: ",current_box.row,current_box.col)
            queried_box = self.environment.QueryMethodBox(current_box)
            self.agent.updateBoxInfo(queried_box)
        self.mineFieldSketch(self.environment.mineField)

    # Function to play minesweeper if the number of mines has already been passed as an argument
    def playMinesweeperGivenNumber(self):
        self.agent = Agent(self.dimension, self.numberOfMines)
        current_box = self.agent.pickABox()
        while self.agent.solvedBoxes < self.dimension ** 2:
            print(self.agent.unseenBoxes, self.agent.solvedBoxes)
            print("Query: ", current_box.row, current_box.col)
            queried_box = self.environment.QueryMethodBox(current_box)
            self.agent.updateBoxInfo(queried_box)
            current_box = self.agent.pickABox()
        self.mineFieldSketch(self.environment.mineField)



if __name__ == "__main__":
    mp = MainProgram()

    # # run first time
    # clock()
    #
    # root.mainloop()
