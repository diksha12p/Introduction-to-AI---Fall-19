import matplotlib.pyplot as plt
import pandas as pd

# List containing predefined number of mines
number_of_mines = [2, 4, 6, 8, 10, 12, 14, 16]

data_MinesweeperWithMines = pd.read_csv("MinesweeperStatsWithMines.csv")
data_Minesweeper = pd.read_csv("MinesweeperStats.csv")

# Defining lists to store the final output
FinalScoreAverage = []
FinalScoreAverage_withMines = []

# Looping through every given number in the list of 'number_of_mines'
for mine_number in number_of_mines:
    dfScore = data_Minesweeper.loc[data_Minesweeper["NumberOfMines"] == mine_number]
    FinalScoreAverage.append(dfScore["FinalScore"].mean())

    dfScoreWithMines = data_MinesweeperWithMines.loc[data_MinesweeperWithMines["NumberOfMines"] == mine_number]
    FinalScoreAverage_withMines.append(dfScoreWithMines["FinalScore"].mean())

# Plotting the final graphs - WITHOUT PASSING NUMBER OF MINES
plt.plot(number_of_mines, FinalScoreAverage, color='blue', label="Original Scores")
# Plotting the final graphs - WITH PASSING NUMBER OF MINES
plt.plot(number_of_mines, FinalScoreAverage_withMines, color='red', label="Scores after providing Number of Mines")

plt.xlabel('Number Of Mines')
plt.ylabel('Final Average Score')
plt.title('Mine Density vs Final Average Score ')

plt.legend()
"""
To obtain ONLY the graph when no mines are passed,
Comment line numbers 19, 20, 25 and 37 & uncomment line number 36
"""
# plt.savefig('ScoreWithoutMines_test.png')
plt.savefig('ScoreWithMines_test.png')
plt.show()