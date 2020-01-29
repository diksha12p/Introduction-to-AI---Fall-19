# import time
from Environment import *
from Agent import *
import pandas as pd

# Variable definition
IS_MINE = True
count = 0
dimension = 8
number_of_mines = [6, 8, 10, 12, 14, 16]

data_Minesweeper = []
data_MinesweeperWithMines = []

# SCORE : Ratio of total number of identified mines to the total number of mines

# Running and exporting the statistics for the case when the number of mines is unknown to the agent
while count < 10:
    print("Running Instance Number: ", count)
    for number in number_of_mines:
        environment = Environment(dimension, number)
        # No probability is passed to the Agent
        agent = Agent(dimension, -1)
        current_box = agent.pickABox()

        while agent.solvedBoxes < dimension ** 2:
            queried_box = environment.QueryMethodBox(current_box)
            agent.updateBoxInfo(queried_box)
            current_box = agent.pickABox()
        total_identified_mines = 0

        for row in range(dimension):
            for col in range(dimension):

                if agent.agentObservedMineField[row][col].mineFlag == IS_MINE and environment.mineField[row][col].mine == IS_MINE:
                    total_identified_mines += 1

        print(total_identified_mines)
        # Appending "Dimension", "Number Of Mines" & "Final Score"to the list "data_Minesweeper"
        data_Minesweeper.append([dimension, number, float(total_identified_mines / number)])
    count += 1

dataframe_MineSweeper = pd.DataFrame(data_Minesweeper, columns = ["Dimension", "NumberOfMines", "FinalScore"])
dataframe_MineSweeper.to_csv("MinesweeperStats.csv", sep=',', encoding='utf-8', mode='a')

# Running and exporting the statistics for the case when the number of mines is known to the agent
count = 0
while count < 10:
    print("Running Instance Number: ", count)
    for number in number_of_mines:
        environment = Environment(dimension, number)
        agent = Agent(dimension, number)
        current_box = agent.pickABox()
        while agent.solvedBoxes < dimension ** 2:
            queried_box = environment.QueryMethodBox(current_box)
            agent.updateBoxInfo(queried_box)
            current_box = agent.pickABox()
        total_identified_mines = 0

        for row in range(dimension):
            for col in range(dimension):

                if agent.agentObservedMineField[row][col].mineFlag == IS_MINE and environment.mineField[row][col].mine == IS_MINE:
                    total_identified_mines += 1

        print(total_identified_mines)
        # Appending "Dimension", "Number Of Mines" & "Final Score"to the list "data_MinesweeperWithMines"
        data_MinesweeperWithMines.append([dimension, number, float(total_identified_mines / number)])
    count += 1

dataframe_MineSweeperWithMines = pd.DataFrame(data_MinesweeperWithMines, columns=["Dimension", "NumberOfMines", "FinalScore"])
dataframe_MineSweeperWithMines.to_csv("MinesweeperStatsWithMines.csv", sep=',', encoding='utf-8', mode='a')