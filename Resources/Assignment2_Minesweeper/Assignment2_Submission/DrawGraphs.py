import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FinalScoreAverage = []
numberOfMines = [2, 4, 6, 8, 10, 12, 14, 16]
dataMinesweeperWithMines = pd.read_csv("MinesweeperStatsWithMines.csv")
FinalScoreAverageWithMines = []
dataMinesweeper = pd.read_csv("MinesweeperStats.csv")
for number in numberOfMines:
    dfScore = dataMinesweeper.loc[dataMinesweeper["NumberOfMines"] == number]
    FinalScoreAverage.append(dfScore["FinalScore"].mean())
    dfScoreWithMines = dataMinesweeperWithMines.loc[dataMinesweeperWithMines["NumberOfMines"] == number]
    FinalScoreAverageWithMines.append(dfScoreWithMines["FinalScore"].mean())

plt.plot(numberOfMines, FinalScoreAverageWithMines, color='green', label="Scores after providing Number of Mines")
plt.plot(numberOfMines, FinalScoreAverage, color='orange', label="Original Scores")
plt.xlabel('Number Of Mines')
plt.ylabel('Final Average Score')
plt.title('Mine Density vs Final Average Score ')
plt.legend()
plt.show()

