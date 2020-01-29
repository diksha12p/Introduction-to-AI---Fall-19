import CreateMaze
import SolveMaze
import time
import pandas as pd
import numpy as np


# To export all the generated statistics to a CSV
def generateStatistics(object, n, dim):
        # Initial Values
        n=100
        dim=50

        # Variables to store data
        dataDFS=[]
        dataBFS=[]
        dataManhattan=[]
        dataEuclidean=[]

        # List of pre-defined probabilities
        probabilities_list=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

        for probability in probabilities_list:
            for counter in range(n):
                maze=CreateMaze.generateMazeValues(probability,dim)
                start = time.time()
                result = SolveMaze.DFS(maze)
                end = time.time()
                t=end-start
                dataDFS.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

                start = time.time()
                result = SolveMaze.BFS(maze)
                end = time.time()
                t=end-start
                dataBFS.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

                start = time.time()
                result = SolveMaze.astar(maze,"Manhattan")
                end = time.time()
                t=end-start
                dataManhattan.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

                start = time.time()
                result = SolveMaze.astar(maze,"Euclidean")
                end = time.time()
                t=end-start
                dataEuclidean.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])
                
                
        statsDFS=pd.DataFrame(dataDFS,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
        statsDFS.to_csv("DFS_Statistics.csv", sep=',', encoding='utf-8',mode='a')

        statsBFS=pd.DataFrame(dataBFS,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
        statsBFS.to_csv("BFS_Statistics.csv", sep=',', encoding='utf-8',mode='a')

        statsManhattan=pd.DataFrame(dataManhattan,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
        statsManhattan.to_csv("astar_Manhattan_Statistics.csv", sep=',', encoding='utf-8',mode='a')

        statsEuclidean=pd.DataFrame(dataEuclidean,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
        statsEuclidean.to_csv("astar_Euclidean_Statistics.csv", sep=',', encoding='utf-8',mode='a')

        DimTime()
        # AstarMazeThinningStatistics()
        return None

#Dimension vs Time Statistics for all algorithms for a range of dimensions
def DimTime():
    probabilities=[0.1,0.2,0.3,0.4]

    dataDFS=[]
    dataBFS=[]
    dataManhattan=[]
    dataEuclidean=[]

    dimensions=[10,15,20,25,50,75,100,200,400,500]
    for probability in probabilities:
        for dim in dimensions:
            maze=CreateMaze.generateMazeValues(probability,dim)

            start = time.time()
            result = SolveMaze.DFS(maze)
            end = time.time()
            t=end-start
            dataDFS.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

            start = time.time()
            result = SolveMaze.BFS(maze)
            end = time.time()
            t=end-start
            dataBFS.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

            start = time.time()
            result = SolveMaze.astar(maze,"Manhattan")
            end = time.time()
            t=end-start
            dataManhattan.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])

            start = time.time()
            result = SolveMaze.astar(maze,"Euclidean")
            end = time.time()
            t=end-start
            dataEuclidean.append([dim,probability,result.nodes_visited,result.path_length,result.solvable,t])
        
    statsDFS=pd.DataFrame(dataDFS,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
    statsDFS.to_csv("DFS_StatisticsDimension.csv", sep=',', encoding='utf-8',mode='a')

    statsBFS=pd.DataFrame(dataBFS,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
    statsBFS.to_csv("BFS_StatisticsDimension.csv", sep=',', encoding='utf-8',mode='a')

    statsManhattan=pd.DataFrame(dataManhattan,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
    statsManhattan.to_csv("astar_Manhattan_StatisticsDimension.csv", sep=',', encoding='utf-8',mode='a')

    statsEuclidean=pd.DataFrame(dataEuclidean,columns=["Dimension","Probability","Number_of_nodes_visited","Path_Length","Solvable","Time"])
    statsEuclidean.to_csv("astar_Euclidean_StatisticsDimension.csv", sep=',', encoding='utf-8',mode='a')
        
    return None
