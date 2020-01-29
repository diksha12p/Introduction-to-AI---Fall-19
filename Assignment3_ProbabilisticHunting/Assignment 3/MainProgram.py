from Tkinter import *
from Environment import Environment
from Agent import Agent

# Default Value
given_dimension = 50


class MainProgram:
    def __init__(self):
        self.dimension = given_dimension
        self.env = Environment(self.dimension)
        self.agent = None

        # Tkinter window for visualization
        self.window = Tk()
        self.window.title("Probabilistic Search (and Destroy)")
        self.window.geometry('1000x800+200+10')

        # Control Frame definition
        self.controlFrame = Frame(self.window, height=800)
        self.controlFrame.pack(side=LEFT)

        self.rule = IntVar()
        rule_1 = Radiobutton(self.controlFrame, text="RULE - 1", variable=self.rule, value=1, padx=2, pady=2)
        rule_1.pack()

        rule_2 = Radiobutton(self.controlFrame, text="RULE - 2", variable=self.rule, value=2, padx=2, pady=2)
        rule_2.pack()

        self.solveButton = Button(self.controlFrame, text="Locate Target", height=2, width=10, command=self.solve_field)
        self.solveButton.pack()

        # Frame for drawing the field
        self.mazeFrame = Frame(self.window, width=800, height=800)
        self.mazeFrame.pack(side=RIGHT)

        self.mazeCanvas = Canvas(self.mazeFrame, width=800, height=800)
        self.mazeCanvas.pack()
        self.draw_maze()
        self.window.mainloop()

    def solve_field(self):
        self.agent = Agent(self.env, self.rule.get(), self.dimension)

    def draw_maze(self):
        tile_height = 780 / self.dimension
        tile_width = 780 / self.dimension
        # Clear the canvas
        self.mazeCanvas.delete("all")

        self.tiles = [[self.mazeCanvas.create_rectangle(10 + i * tile_width, 10 + j * tile_height,
                                                        10 + (i + 1) * tile_width, 10 + (j + 1) * tile_height) for i in
                       range(self.dimension)] for j in range(self.dimension)]

        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.env.grid[i][j].type == 1:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#90EE90")
                elif self.env.grid[i][j].type == 2:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#32CD32")
                elif self.env.grid[i][j].type == 3:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#228B22")
                elif self.env.grid[i][j].type == 4:
                    self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#006400")


if __name__ == "__main__":
    ms = MainProgram()
