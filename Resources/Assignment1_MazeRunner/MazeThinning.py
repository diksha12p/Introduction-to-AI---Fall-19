# -*- coding: utf-8 -*-
"""
@author: Sharvani Pratinidhi
"""
from copy import deepcopy
import random
from math import sqrt
#Program to Implement Maze Thinning
class ResultAStar:
    def __init__(self,NodeMaze,maze,nodes_visited,path_length,solvable):
        self.NodeMaze=NodeMaze
        self.maze=maze
        self.nodes_visited=nodes_visited
        self.path_length=path_length
        self.solvable=solvable
        
class astarNode():
    def __init__(self, parent, x,y):
       self.parent = parent
       self.x=x
       self.y=y
       self.g_score = 0
       self.h_score = 0
       self.f_score = 0

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
    
def createNodeMazeAstar(maze,dim):
    astarNodeMaze = [[astarNode(None,i,j) for j in range(dim)] for i in range(dim)]
    return astarNodeMaze  

def MazeThinner(dim,thinMaze,q):
    
    for i in range(dim):
        for j in range(dim):
            if thinMaze[i][j]==1:
                if random.random()<q:
                    thinMaze[i][j]=0
    result=astar(thinMaze,dim,"Manhattan",0)
    
    return result.NodeMaze   

def astar(maze,dim,heuristic,q):
    a_maze=deepcopy(maze)
    thinMaze=deepcopy(maze)
    astarNodeMaze=createNodeMazeAstar(maze,dim)
    
    if heuristic=="Manhattan":
        heuristic_function=heuristic_Manhattan_Distance
    elif heuristic=="Euclidean":
        heuristic_function=heuristic_Euclidean_Distance
    else:
        heuristic_function=None
        ThinNodeMaze=MazeThinner(dim,thinMaze,q)
        for i in range(dim-1):
            for j in range(dim-1):
                astarNodeMaze[i][j].h_score=ThinNodeMaze[i][j].f_score

    a_maze[0][0] = 0
    a_maze[dim-1][dim-1] = 0
    number_nodes_visited=0
    start_node =astarNodeMaze[0][0]
    end_node = astarNodeMaze[dim-1][dim-1]
    
    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        curr_node = open_list[0]
        curr_index = 0
        for index, item in enumerate(open_list):
            if item.f_score < curr_node.f_score:
                curr_node = item
                curr_index = index

        open_list.pop(curr_index)
        closed_list.append(curr_node)
        number_nodes_visited+=1
        if curr_node == end_node:
            path = []
            current = curr_node
            while current is not start_node:
                path.append(current)
                a_maze[current.x][current.y]=5                
                current = current.parent
           
            return ResultAStar(astarNodeMaze,a_maze,number_nodes_visited,len(path),1)
        children = []
        for neighbour in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            node_position = (curr_node.x + neighbour[0], curr_node.y + neighbour[1])

            if node_position[0] > (dim - 1) or node_position[0] < 0 or node_position[1] > (dim -1) or node_position[1] < 0:
                continue

            if a_maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = astarNodeMaze[node_position[0]][node_position[1]]
            new_node.parent=curr_node
            
            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g_score = curr_node.g_score + 1
            if(heuristic_function==heuristic_Euclidean_Distance or heuristic_function==heuristic_Manhattan_Distance):
                child.h_score =  heuristic_function(child,end_node)
            child.f_score = child.g_score + child.h_score

            for open_node in open_list:
                if child == open_node and child.g_score > open_node.g_score:
                    continue

            open_list.append(child)
            a_maze[child.x][child.y]=7
            
    return ResultAStar(astarNodeMaze,a_maze,number_nodes_visited,0,0)

def heuristic_Euclidean_Distance(a, b):
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def heuristic_Manhattan_Distance(a,b):
    return abs((b.x - a.x)) + abs((b.y - a.y))    