from collections import deque
from copy import deepcopy
from math import sqrt
class Result(object):
    def __init__(self,maze,nodes_visited,path_length,solvable,max_fringe_size):
        self.maze=maze
        self.nodes_visited=nodes_visited
        self.path_length=path_length
        self.solvable=solvable
        self.max_fringe_size = max_fringe_size
        # solvable is 1 if the maze is solvable, else 0
    
class Node(object):
    def __init__(self, x, y,value):
        self.x = x
        self.y = y
        self.parent = None
        self.visited = False
        self.value=value
                
    
    def goal_State(self,maze):
        if(self.x == len(maze) -1 and self.y == len(maze)- 1):
            return True
        return False
        
    def getNeighbors(self,nodeMaze):
        x = self.x
        y = self.y
        neighbors = list()
        if(x+1<len(nodeMaze)):
            if(nodeMaze[x+1][y].visited==False and nodeMaze[x+1][y].value!=1):
                neighbors.append(nodeMaze[x+1][y])
        
        if(y+1<len(nodeMaze)):
            if(nodeMaze[x][y+1].visited==False and nodeMaze[x][y+1].value!=1):
                neighbors.append(nodeMaze[x][y+1])
        
        if(x-1>=0):
            if(nodeMaze[x-1][y].visited==False and nodeMaze[x-1][y].value!=1):
                neighbors.append(nodeMaze[x-1][y])
                
        if(y-1>=0):
            if(nodeMaze[x][y-1].visited==False and nodeMaze[x][y-1].value!=1):
                neighbors.append(nodeMaze[x][y-1])
        
        return neighbors
        

    
class stack(list):
    def push(self, item):
        self.append(item)
   
class Queue(deque):
    def enqueue(self, item):
        self.append(item)
    def dequeue(self):
        return self.popleft()
        
def pathFollowed(node):
    if node == None:
        return None
    current = node
    path = list()
    path.append(node)
    while current.parent != None:
        current = current.parent
        path.append(current)
    #print(len(path))
    return path

def createNodeMaze(maze):
    dim=len(maze)
    NodeMaze = [[Node(i,j,maze[i][j]) for j in range(dim)] for i in range(dim)]
    return NodeMaze
    
def DFS(maze):
    number_nodes_visited=0
    DFSmaze=deepcopy(maze)
    nodeMaze=createNodeMaze(maze)
    s=nodeMaze[0][0]
    s.visited=True
    DFSstack=stack()
    DFSstack.push(s)
    max_fringesize = 1
    while(DFSstack):
        s=DFSstack.pop()
        #print(s.x,",",s.y)
        number_nodes_visited+=1
        #print(number_nodes_visited)
        DFSmaze[s.x][s.y]=7
        if(s.goal_State(DFSmaze)):
            path=pathFollowed(s)
            for p in path:
                DFSmaze[p.x][p.y]=5
            return Result(DFSmaze,number_nodes_visited,len(path),1,max_fringesize)
            
        for neighbor in (s.getNeighbors(nodeMaze)):
            neighbor.parent = s
            neighbor.visited = True
            DFSstack.push(neighbor)
        
        fringesize = len(DFSstack) 
        if fringesize > max_fringesize:
            max_fringesize = fringesize
    
    return Result(DFSmaze,number_nodes_visited,0,0,max_fringesize)
        
def BFS(maze):
    number_nodes_visited=0
    BFSmaze=deepcopy(maze)
    nodeMaze=createNodeMaze(maze)
    s=nodeMaze[0][0]
    BFSQueue=Queue()
    BFSQueue.enqueue(s)
    max_fringesize = 1
    s.visited=True
    while(BFSQueue):
        s=BFSQueue.dequeue()
        #print(s.x,",",s.y)
        number_nodes_visited+=1
        #print(number_nodes_visited)
        BFSmaze[s.x][s.y]=7
        if(s.goal_State(BFSmaze)):
            path=pathFollowed(s)
            for p in path:
                BFSmaze[p.x][p.y]=5
            return Result(BFSmaze,number_nodes_visited,len(path),1,max_fringesize)
        for neighbor in (s.getNeighbors(nodeMaze)):
            neighbor.parent = s
            neighbor.visited = True
            BFSQueue.enqueue(neighbor)
        
        fringesize = len(BFSQueue) 
        if fringesize > max_fringesize:
            max_fringesize = fringesize
    
    
    return Result(BFSmaze,number_nodes_visited,0,0,max_fringesize)
    
class aNode():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0

    def __eq__(self, other):
        return self.position == other.position
                
        
    
def astar(maze,heuristic):
    a_maze=deepcopy(maze)
    if heuristic=="Manhattan":
        heuristic_function=heuristic_Manhattan_Distance
    else:
        heuristic_function=heuristic_Euclidean_Distance
    start = (0,0)
    end = (len(maze)-1,len(maze)-1)
    a_maze[0][0] = 0
    a_maze[len(a_maze)-1][len(a_maze)-1] = 0
    number_nodes_visited=0
    start_node = aNode(None, start)
    end_node = aNode(None, end)
    open_list = []
    closed_list = []

    open_list.append(start_node)
    max_fringesize = 1
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
            while current is not None:
                path.append(current.position)
                a_maze[current.position[0]][current.position[1]]=5                
                current = current.parent

            return Result(a_maze,number_nodes_visited,len(path),1,max_fringesize)
        children = []
        for neighbour in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            node_position = (curr_node.position[0] + neighbour[0], curr_node.position[1] + neighbour[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if a_maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = aNode(curr_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g_score = curr_node.g_score + 1
            child.h_score =  heuristic_function(child,end_node)
            child.f_score = child.g_score + child.h_score

            for open_node in open_list:
                if child == open_node and child.g_score > open_node.g_score:
                    continue

            open_list.append(child)
            fringesize = len(open_list) 
            if fringesize > max_fringesize:
                max_fringesize = fringesize
            a_maze[child.position[0]][child.position[1]]=7
            
            
    return Result(a_maze,number_nodes_visited,0,0,max_fringesize)
            
def heuristic_Euclidean_Distance(a, b):
    return sqrt((b.position[0] - a.position[0]) ** 2 + (b.position[1] - a.position[1]) ** 2)

def heuristic_Manhattan_Distance(a,b):
    return abs((b.position[0] - a.position[0])) + abs((b.position[1] - a.position[1]))    