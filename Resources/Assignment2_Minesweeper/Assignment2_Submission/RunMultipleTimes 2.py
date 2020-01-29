# import time
from Environment import *
from Agent import *
import numpy as np
import pandas as pd

IS_MINE = True
count = 0
dimension = 8
numberOfMines = [6, 8, 10, 12, 14, 16]
dataMinesweeper = []
dataMinesweeperWithMines=[]

while count < 10:
    print("Count",count)
    for number in numberOfMines:
        #print("Running Instance:", count)
        env = Environment(dimension, number)
        agent = Agent(dimension,-1)
        currentBox = agent.selectABox()
        while agent.solvedBoxes < dimension ** 2:
            #print("Query: ", currentBox.row, currentBox.col)
            queriedBox = env.queryBox(currentBox)
            agent.updateBox(queriedBox)
            currentBox = agent.selectABox()
        numberOfIdentifiedMines = 0
        for row in range(dimension):
            for col in range(dimension):

                if (agent.observedMineField[row][col].mineFlag == IS_MINE and env.mineField[row][col].mine == IS_MINE):
                    #print(row,col)
                    numberOfIdentifiedMines += 1

        print(numberOfIdentifiedMines)
        dataMinesweeper.append([dimension, number, float(numberOfIdentifiedMines / number)])
    count += 1

DFMinesweeper = pd.DataFrame(dataMinesweeper,
                             columns=["Dimension", "NumberOfMines", "FinalScore"])
DFMinesweeper.to_csv("MinesweeperStats.csv", sep=',', encoding='utf-8', mode='a')

count = 0
while count < 10:
    print("Count",count)
    for number in numberOfMines:
        #print("Running Instance:", count)
        env = Environment(dimension, number)
        agent = Agent(dimension,number)
        currentBox = agent.selectABox()
        while agent.solvedBoxes < dimension ** 2:
            #print("Query: ", currentBox.row, currentBox.col)
            queriedBox = env.queryBox(currentBox)
            agent.updateBox(queriedBox)
            currentBox = agent.selectABox()
        numberOfIdentifiedMines = 0
        for row in range(dimension):
            for col in range(dimension):

                if (agent.observedMineField[row][col].mineFlag == IS_MINE and env.mineField[row][col].mine == IS_MINE):
                    #print(row,col)
                    numberOfIdentifiedMines += 1

        print(numberOfIdentifiedMines)
        dataMinesweeperWithMines.append([dimension, number, float(numberOfIdentifiedMines / number)])
    count += 1

DFMinesweeperWithMines = pd.DataFrame(dataMinesweeperWithMines,
                             columns=["Dimension", "NumberOfMines", "FinalScore"])
DFMinesweeperWithMines.to_csv("MinesweeperStatsWithMines.csv", sep=',', encoding='utf-8', mode='a')