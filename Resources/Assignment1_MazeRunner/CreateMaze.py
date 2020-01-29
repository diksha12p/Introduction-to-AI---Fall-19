from tkinter import *
import random
import numbers
import SolveMaze
import simulated_annealing
import time
import numpy as np
import pandas as pd
import StatisticsGenerator
import MazeThinning

# Default starting values
dimensions=10
probability=0.3

# Function to generate a maze of [dim][dim] dimensions
def generateMazeValues(prob,dim):
    grid=[ [0]*dim for _ in range(dim) ]
    for i in range(dim):
        for j in range(dim):
            if random.random() < prob:
                 grid[i][j] = 1
                 
    grid[0][0] = 2
    grid[dim - 1][dim - 1] = 3

    #print(grid)
    return grid


class Maze(object):

    def __init__(self):
        self.dimension = dimensions
        self.prob = probability
        self.grid=[[0] * self.dimension for _ in range(self.dimension)]

        self.window = Tk()
        self.window.title("Maze Simulator")
        self.window.geometry('1200x800+200+25')

        # Frame for options
        self.controlFrame=Frame(self.window,height=700)
        self.controlFrame.pack(side=LEFT)

        self.labelDim=Label(self.controlFrame,text='Dimensions', fg = "red", font = "Times")
        self.labelDim.pack()

        self.entryDim=Entry(self.controlFrame)
        self.entryDim.pack()

        self.labelProb=Label(self.controlFrame,text='Probability', fg = "red", font = "Times")
        self.labelProb.pack()

        self.entryProb=Entry(self.controlFrame)
        self.entryProb.pack()

        self.createMazeButton = Button(self.controlFrame, text="Create Maze", command=self.create_Maze, fg ="black", font ="Times")
        self.createMazeButton.pack()

        self.DFSButton = Button(self.controlFrame, text="DFS", command=self.drawSolutionDFS, fg ="red", font ="Times")
        self.DFSButton.pack()

        self.BFSButton=Button(self.controlFrame, text="BFS", command=self.drawSolutionBFS, fg ="red", font ="Times")
        self.BFSButton.pack()

        self.AStarManhattanButton=Button(self.controlFrame, text="A* Manhattan Heuristic", command=self.drawSolutionAStarManhattan, fg ="red", font ="Times")
        self.AStarManhattanButton.pack()
        
        self.AStarEuclideanButton=Button(self.controlFrame, text="A* Euclidean Heuristic", command=self.drawSolutionAStarEuclidean, fg ="red", font ="Times")
        self.AStarEuclideanButton.pack()

        # Bi-directional BFS part comes here
        # self.BiDirectionalBFSButton = Button(self.controlFrame, text="Bi-Directional BFS", command=self. ???????????????????????? , fg="red", font="Times")
        # self.BiDirectionalBFSButton.pack()

        self.generateStatsButton=Button(self.controlFrame, text="Generate Statistics", command=self.runStats, fg="red", font ="Times")
        self.generateStatsButton.pack()
        
        """
        Choice of method for 'Path Planning' among the following METHOD:
        1. Depth First Search (DFS)
        2. Breadth First Search (BFS)
        3. A-Star with Eucledian Distance as Heuristic
        4. A-Star with Manhattan Distance as Heuristic
        5. Bi-directional BFS
        """
        self.methodChoiceLabel=Label(self.controlFrame, text='Method', fg ="red", font ="Times")
        self.methodChoiceLabel.pack()
        self.input1 = StringVar(self.controlFrame)
        # Initial value
        self.input1.set("")
        self.option_input1 = OptionMenu(self.controlFrame, self.input1, "DFS", "A* with Manhattan")
        self.option_input1.pack()
        print(self.input1.get())

        """
        Selection of the hardest maze using the following two METRIC:
        1. DFS with Maximum Fringe Size 
        2. A* Manhattan with Maximum nodes 
        """
        self.labelMetric=Label(self.controlFrame,text='Metric', fg = "red", font = "Times")
        self.labelMetric.pack()
        self.var2 = StringVar(self.controlFrame)
        self.var2.set("") # initial value
        self.option2 = OptionMenu(self.controlFrame, self.var2, "Maximum number of Nodes Expanded","Maximum Fringe Size")
        self.option2.pack()
        
        # Local Search Algorithm (Simulated Annealing) employed for finding the 'Hard Maze'
        self.localSearchButton=Button(self.controlFrame, text="Local Search Algorithm", command=self.simulated_annealing, fg ="red", font ="Times")
        self.localSearchButton.pack()
        
        # Frame for drawing the Maze
        self.mazeFrame=Frame(self.window, width=700, height=700)
        self.mazeFrame.pack(side=RIGHT)

        self.mazeCanvas=Canvas(self.mazeFrame, width=700, height=700)
        self.mazeCanvas.pack()

        self.window.mainloop()
    
    # Call to 'Simulated Annealing' : our local search algorithm
    def simulated_annealing(self):
 
        input_option1 = self.input1.get()
        if(input_option1 == "DFS"):
            method = "1"
        else:
            method = "3"

        input_option2 = self.var2.get()
        if input_option2 == "Number of Nodes Expanded":
            metric = "2"
        else:
            metric = "3"
        
        hard_Maze = simulated_annealing.simulated_Annealing(self.grid, method, metric)

        self.paintMyMaze(hard_Maze)
    
    # Get values from the entries and check their validity to then generate the maze
    def generateMaze(self):
        self.prob=self.entryProb.get()
        self.dimension=self.entryDim.get()
        try:
           self.prob=float(self.entryProb.get())
           self.dimension=int(self.entryDim.get())
        except ValueError:
            print ("Invalid parameters !! ")
            return None
        if self.prob <= 0 and self.prob > 1:
            print ("Invalid parameter: " + str(self.prob))
            return None
        self.grid=generateMazeValues(self.prob, self.dimension)
    
    # Run the program multiple times to generate the statistics
    def runStats(self):
       result = StatisticsGenerator.generateStatistics(self, 100, 10)
    
    # To generate and draw maze
    def create_Maze(self):
        self.generateMaze()
        self.paintMyMaze(self.grid)

# Calls to functions in SolveMaze.py to obtain solutions
    def drawSolutionDFS(self):
        result=SolveMaze.DFS(self.grid)
        print(result.maze)
        self.paintMyMaze(result.maze)

    def drawSolutionBFS(self):
        result=SolveMaze.BFS(self.grid)
        print(result.maze)
        self.paintMyMaze(result.maze)

    def drawSolutionAStarManhattan(self):
        result=SolveMaze.astar(self.grid,"Manhattan")
        print(result.maze)
        self.paintMyMaze(result.maze)

    def drawSolutionAStarEuclidean(self):
        result=SolveMaze.astar(self.grid,"Euclidean")
        print(result.maze)
        self.paintMyMaze(result.maze)
        
#To actually draw the maze on frame
    def paintMyMaze(self, maze):
        height_tile = (680) // self.dimension
        width_tile = (680) // self.dimension
        # Clear the canvas
        self.mazeCanvas.delete("all")
        self.tiles = [[self.mazeCanvas.create_rectangle(10 + i * width_tile, 10 + j * height_tile, 10 + (i + 1) * width_tile,
                                                        10 + (j + 1) * height_tile) for i in range(self.dimension)] for j in range(self.dimension)]

        for i in range(self.dimension):
            for j in range(self.dimension):
                if maze[i][j] == 1:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill = "#000000")
                elif maze[i][j] == 5:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill = "#F08080")
                elif maze[i][j] == 7:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill = "#C0C0C0")
        self.mazeCanvas.itemconfig(self.tiles[0][0], fill = "#ff0000")
        self.mazeCanvas.itemconfig(self.tiles[self.dimension - 1][self.dimension - 1], fill ="#008000")

if __name__=="__main__":
    maze_obj1=Maze()
