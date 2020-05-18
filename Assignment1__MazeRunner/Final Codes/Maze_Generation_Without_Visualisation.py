# GENERATING A MAZE WITH PROBABILITY P
# 1 indicates the cell is free
# 0 indicates the cell is filled

# The Source and the destination cell should always be a zero

#Initialise a matrix of dimension d and fill o
class Maze:
        def __init__(self,probability,dimension):
            # Atrtribute Definition
            self.dimension=dimension
            self.probability=probability
            self.array = np.ones((self.dimension, self.dimension), dtype=np.int32).tolist()
            self.source=0
            self.destination=(dimension*dimension)-1
            self.stop_point=0


            # Deepcopy to obtain another array for 'colour_it' and 'paint_my_maze' functions
            self.temp = deepcopy(self.array)

#             # Tkinter specific window commands for title and window size
#             self.window = Tk()
#             self.window.title("Maze Simulator")
#             self.window.geometry('900x700+200+10')

#             # Frame for options
#             self.controlFrame = Frame(self.window, height=700)
#             self.controlFrame.pack(side=LEFT)

#             self.labelDim = Label(self.controlFrame, text='Dimensions')
#             self.labelDim.pack()

#             self.entryDim = Entry(self.controlFrame)
#             self.entryDim.pack()

#             self.labelProb = Label(self.controlFrame, text='Probability')
#             self.labelProb.pack()

#             self.entryProb = Entry(self.controlFrame)
#             self.entryProb.pack()

#             self.createMazeButton = Button(self.controlFrame, text="Create Maze", command=self.create_Maze, fg="black", font="Times")
#             self.createMazeButton.pack()

#             self.BFSButton = Button(self.controlFrame, text="BFS", command=self.BFS, fg="red", font="Times")
#             self.BFSButton.pack()

#             self.BFSButton = Button(self.controlFrame, text="DFS", command=self.DFS, fg="red", font="Times")
#             self.BFSButton.pack()

#             self.BFSButton = Button(self.controlFrame, text="A* with Manhattan", command=self.Astar_Euc, fg="red", font="Times")
#             self.BFSButton.pack()

#             self.BFSButton = Button(self.controlFrame, text="A* with Eucledian", command=self.Astar_Man, fg="red", font="Times")
#             self.BFSButton.pack()

#             self.BFSButton = Button(self.controlFrame, text="Bi-directional BFS", command=self.Bidirectional_BFS, fg="red", font="Times")
#             self.BFSButton.pack()

#             # Frame for drawing the Maze
#             self.mazeFrame = Frame(self.window, width=700, height=700)
#             self.mazeFrame.pack(side=RIGHT)

#             self.mazeCanvas = Canvas(self.mazeFrame, width=700, height=700)
#             self.mazeCanvas.pack()

#             self.window.mainloop()
        
        # Function to initialize the Maze
        def Mazeinitialise(self):

            # Randomly choosing (probability*dimension*dimension) boxes to colour them as filled
            indices = np.random.choice(self.dimension * self.dimension, int(self.probability * self.dimension * self.dimension), replace=False)
            
            # Obtaining the coordinate for the chosen element & assigning zero there i.e. filled
            for ix in indices:
                i, j = divmod(ix, self.dimension)
                self.array[i][j] = 0
            # Start and end are assigned 1 i.e. free
            self.array[0][0]=1
            self.array[self.dimension-1][self.dimension-1]=1
    
        # Print the Maze to the user
        def MazePrint(self):
            for a in self.array:
                print(a)
                
        # Creating the maze for the 'Maze Simulator' window
        def create_Maze(self):
            self.Mazeinitialise()
            self.paint_my_maze(self.array)

        # Function to obtain the 2D coordinates for the given item defined in a 1D list
        def get_coordinates(self, i):
            return divmod(i, self.dimension)

        # Obtain the neighbours i.e top, left, right and bottom for the given item at the given index
        def get_adjacent(self, i, d):
            ret = []
            if abs(i % d - (i + 1) % d) == 1:
                ret.append(i + 1)
            if abs(i % d - (i - 1) % d) == 1:
                ret.append(i - 1)
            if ((i + d) < d * d):
                ret.append(i + d)
            if ((i - d) >= 0):
                ret.append(i - d)
            return ret

        # Function to paint the generated maze in the 'Maze Simulation' window
        def paint_my_maze(self, maze):
            # Defining the tile dimensions for the maze
            tile_width = (680) // self.dimension
            tile_height = (680) // self.dimension
            # Clear the canvas for every new session
            self.mazeCanvas.delete("all")
            self.tiles = [[self.mazeCanvas.create_rectangle(10 + i * tile_width,
                                                                10 + j * tile_height, 10 + (i + 1) * tile_width,
                                                                10 + (j + 1) *
                                                                tile_height) for i in range(self.dimension)] for j in
                              range(self.dimension)]

            """
            Fill the tile colour according to the conditions satisfied where the legend is:
            0: Starting block
            4: Final path blocks
            3: Visited blocks
            1: Restricted blocks
            """

            for i in range(self.dimension):
                for j in range(self.dimension):
                    if maze[i][j] == 0:
                        self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#000000")
                    elif maze[i][j] == 3:
                        self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#C0C0C0")
                    elif maze[i][j] == 1:
                        self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#FFD700")
                    elif maze[i][j] == 4:
                        self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#00008B")
                    elif maze[i][j] == 8:
                        self.mazeCanvas.itemconfig(self.tiles[i][j], fill="#FA8072")
            self.mazeCanvas.itemconfig(self.tiles[0][0], fill="#ff0000")
            self.mazeCanvas.itemconfig(self.tiles[self.dimension - 1][self.dimension - 1], fill="#228b22")

        """

        Algorithm defined : Breadth First Search 

        """
        def BFS(self):
            # Defining an array to keep a track of the visited nodes
            self.BFS_visited= [False] * (self.dimension*self.dimension)
            queue=[]
            
            self.path_possible_BFS=99

            # Defining the start as the source node i.e. (0,0)
            start = self.source
            
            # Appending the 'start' node to the Queue and setting its visited flag as 'True'
            queue.append(start)
            self.BFS_visited[start]=True
            
            # Defining a dictionary to keep a track of parent node of each of the nodes explored
            self.BFS_dic={}
            
            # List to store the path from start to destination
            self.BFS_path =[]

            print("\nBFS Traversal is as below")
            while queue:
                start = queue.pop(0)
                # Generate the 2D coordinates from the 1D list
                a,b=self.get_coordinates(start)
                print ("\n","Node Explored ", start," ","Its Coordinates are",a,",",b, end = " ")  
                # Looping through the neighbours for the chosen node
                for i in self.get_adjacent(start,self.dimension):
                    # Visit only if not visited before
                    if i not in self.BFS_dic.keys():
                        self.BFS_dic[i]=start
                    p, q = self.get_coordinates(i)
                    if self.array[p][q] == 1:
                        if self.BFS_visited[i] == False:
                            queue.append(i)
                            self.BFS_visited[i] = True
                    else:
                        continue
            self.BFS_path = self.get_BFS_path()
            
            # self.result_BFS = self.colour_it(self.BFS_path, self.BFS_visited)
            # self.paint_my_maze(self.result_BFS)

                        
        # This function is called after BFS traversal is done. It returns the shortest path to reach the given destination
        def get_BFS_path(self):
            path=[]
            t=self.destination

            # We recursively keep calling this function until we reach the source from destination
            while(t!=self.source):
                path.append(t)
                if t in self.BFS_dic.keys():
                    t=self.BFS_dic[t]
                else:
                    self.path_possible_BFS=0
                    print("\n Path Not possible")
                    return

            #Flag to update if there is a possible path
            self.path_possible_BFS=1
            path.append(self.source)
            path.reverse()
            print("\n\n The Path through BFS from",self.source,"to",self.destination, "is", path)
            self.print_path(path)
            return path

        """

        Algorithm defined : Depth First Search 

        """

        # This function initiates the DFS and also calls the get path and DFS traversal functions inside

        def DFS(self):
            self.DFS_visited = [False] * (self.dimension*self.dimension)
            start = self.source

            #This dictionary stores the parent node for each child visited 
            self.DFS_dic={}

            self.path_possible_DFS=99
            
            #Calling the DFS Traversal function by specifying a start point
            print("\nDFS Traversal is as below")
            self.DFS_trav(start)

            #Calling the DFS get_path function by specifying a start point
            self.DFS_path = self.get_DFS_path()

            # self.result_DFS = self.colour_it(self.DFS_path, self.DFS_visited)
            # self.paint_my_maze(self.result_DFS)

        # This function does the DFS traversal for a given start point. It is recursively called inside.
        def DFS_trav(self, start):
            self.DFS_visited[start] = True
            a,b=self.get_coordinates(start)
            print("\nNode Explored",start,"Its Coordinates are",a, b, end = ' ') 
            
            for i in self.get_adjacent(start,self.dimension):
                if i not in self.DFS_dic.keys():
                    self.DFS_dic[i]=start
                p, q = divmod(i, self.dimension)
                if self.array[p][q] == 1:
                    if self.DFS_visited[i] == False:
                        self.DFS_trav(i)
                    else:
                        continue

                        
        # This function returns the shortest path found through the DFS algorithm
        def get_DFS_path(self):
            path=[]
            t=self.destination

            # We recursively keep calling this function until we reach the source from destination
            while(t!=self.source):
                path.append(t)
                if t in self.DFS_dic.keys():
                    t=self.DFS_dic[t]
                else:
                    self.path_possible_DFS=0
                    print("\n Path Not possible")
                    return

            #Flag to update if there is a possible path
            self.path_possible_DFS=1
            path.append(self.source)
            path.reverse()
            print("\n\n The Path through DFS from",self.source,"to",self.destination, "is", path)
            self.print_path(path)

            return path
            
        #This function calculates the Euclidean distance between two points
        def get_euclidean_dis(self, a, b):
            ax, ay = divmod(a, self.dimension)
            bx, by = divmod(b, self.dimension)
            return math.sqrt(((ax-bx) ** 2) + ((ay-by) **2)) 
                    
        #This function calculates the Manhattan distance between two points
        def get_manhattan_dis(self, a, b):
            ax, ay = divmod(a, self.dimension)
            bx, by = divmod(b, self.dimension)
            return abs(ax-bx)+ abs(ay-by)
        
        #For a given array this calculates the Euclidean & Manhattan Heuristic for all the points
        def Calculate_heuristic(self):
            self.E_heuristic = [0] * (self.dimension ** 2)
            self.M_heuristic = [0] * (self.dimension ** 2)
            for i in range(0,self.dimension ** 2):
                self.E_heuristic[i] = self.get_euclidean_dis(i, (self.dimension ** 2)-1)
                self.M_heuristic[i] = self.get_manhattan_dis(i, (self.dimension ** 2)-1)


        """

        Algorithm defined : A-Star using Euclidean Heuristic 

        """

        #This function calls the A-star traversal & A-star 
        def Astar_Euc(self):
            self.Astar_visited_Euc = [False] * (self.dimension * self.dimension)
            start = self.source
            self.Astar_path_Euc = []
            self.Astar_path_Euc.append(start)
            self.path_possible_Euc = 0

            self.Calculate_heuristic()
            print("\nA-star Traversal Using Euclidean Heuristic is as below")
            self.Astar_trav_Euc(start, self.Astar_visited_Euc, self.E_heuristic)

            if (self.path_possible_Euc == 1):
                print("\n\n The Path through A-Star using Euclidean Heuristic from", self.source, "to",
                      self.destination, "is", self.Astar_path_Euc)
                self.print_path(self.Astar_path_Euc)

            else:
                print("\n\nPath not possible")

            # self.result_Astar_Euc = self.colour_it(self.Astar_path_Euc, self.Astar_visited_Euc)
            # self.paint_my_maze(self.result_Astar_Euc)

        #This function does the A-star Traversal using Euclidean heuristic to choose the next node to be explored
        def Astar_trav_Euc(self, start, visited, Heuristic):
            visited[start] = True
            a, b = self.get_coordinates(start)
            print("\nNode Explored", start, "Its Coordinates are", a, b, end=' ')
            nodes = self.get_adjacent(start, self.dimension)
            nodes_h = [Heuristic[j] for j in nodes]
            for i in [x for _, x in sorted(zip(nodes_h, nodes))]:
                p, q = self.get_coordinates(i)
                if self.array[p][q] == 1:
                    if visited[i] == False:
                        if (i == self.destination):
                            self.Astar_path_Euc.append(i)
                            self.path_possible_Euc = 1
                            return True
                        else:
                            self.Astar_path_Euc.append(i)
                            check = self.Astar_trav_Euc(i, visited, Heuristic)
                            if (check == True):
                                return check
                            else:
                                self.Astar_path_Euc.pop()
                                continue
                    else:
                        return False

        """

        Algorithm defined : A-Star using Manhattan Heuristic 

        """


        #This function calls the A-star Traversal functions
        def Astar_Man(self):
            self.Astar_visited_Man = [False] * (self.dimension * self.dimension)
            start = self.source
            self.path_possible_Man = 0
            self.Astar_path_Man = []
            self.Astar_path_Man.append(start)

            self.Calculate_heuristic()

            print("\n\nA-star Traversal Using Manhattan Heuristic is as below")
            self.Astar_trav_Man(start, self.Astar_visited_Man, self.M_heuristic)

            if (self.path_possible_Man == 1):

                print("\n The Path through A-Star using Manhattan Heuristic from", self.source, "to", self.destination,
                      "is", self.Astar_path_Man)
                self.print_path(self.Astar_path_Man)

            else:
                print("\n\nPath not possible")

            # self.result_Astar_Man = self.colour_it(self.Astar_path_Man, self.Astar_visited_Man)
            # self.paint_my_maze(self.result_Astar_Man)


        #This function does the A-star Traversal using Manhattan heuristic to choose the next node to be explored
        def Astar_trav_Man(self, start, visited, Heuristic):
            visited[start] = True
            a, b = self.get_coordinates(start)
            print("\nNode Explored", start, "Its Coordinates are", a, b, end=' ')
            nodes = self.get_adjacent(start, self.dimension)
            nodes_h = [Heuristic[j] for j in nodes]
            for i in [x for _, x in sorted(zip(nodes_h, nodes))]:
                p, q = self.get_coordinates(i)
                if self.array[p][q] == 1:
                    if visited[i] == False:
                        if (i == self.destination):
                            self.Astar_path_Man.append(i)
                            self.path_possible_Man = 1
                            return True
                        else:
                            self.Astar_path_Man.append(i)
                            check = self.Astar_trav_Man(i, visited, Heuristic)
                            if (check == True):
                                return check
                            else:
                                self.Astar_path_Man.pop()
                                continue
                    else:
                        return False
        """

        Algorithm defined : Bi-Directional BFS 

        """


        #This function initiates the Bi-directional BFS by assigning a start & end point
        def Bidirectional_BFS(self):
            start = self.source
            end = self.destination
            self.Bidirectional_BFS_trav(start, end)
            self.get_Bi_BFS_path()
            
            if (self.Bi_BFS_stop!=99):
                self.path_possible_Bi_BFS=1
            else:
                self.path_possible_Bi_BFS=0

            
            # self.Bi_BFS_visited = self.BFS_visited_left + self.BFS_visited_right

            # self.result_Bi_BFS = self.colour_it_BiBFS(self.path_Bi_BFS, self.BFS_visited_left, self.BFS_visited_right)
            # self.paint_my_maze(self.result_Bi_BFS)

        #This function does the Bi-directional BFS traversal from left as well as right
        def Bidirectional_BFS_trav(self, start, end):
            self.BFS_visited_left = [False] * (self.dimension * self.dimension)
            self.BFS_visited_right = [False] * (self.dimension * self.dimension)
            queue_left = []
            queue_right = []
            self.Bi_BFS_stop = 99

            queue_left.append(start)
            queue_right.append(end)


            #These two dictionaries stores the parent node for each child visited from left & right respectively
            self.Bi_BFS_dic_left = {}
            self.Bi_BFS_dic_right = {}

            #These two lists shows if a node is visited from Left & right respectively
            self.BFS_visited_left[start] = True
            self.BFS_visited_right[start] = True

            print("\nBi-Directional BFS Traversal is as below")
            while queue_left and queue_right:
                start = queue_left.pop(0)
                a, b = self.get_coordinates(start)
                print("\n", "Node Explored from left", start, " ", "Its Coordinates are", a, ",", b, end=" ")
                print("It's neighbors are ", self.get_adjacent(start, self.dimension))

                #Left BFS Traversal from the starting node
                for i in self.get_adjacent(start, self.dimension):
                    if i not in self.Bi_BFS_dic_left.keys():
                        self.Bi_BFS_dic_left[i] = start

                    p, q = self.get_coordinates(i)
                    if self.array[p][q] == 1:
                        if self.BFS_visited_left[i] == False:
                            if self.BFS_visited_right == True:

                                #Stop if left and right traversal intersects at a point
                                print("The search stops at intersection point ", i)
                                self.Bi_BFS_stop = i
                                self.Bi_BFS_dic_left[i] = start
                                return
                            else:
                                queue_left.append(i)
                                self.BFS_visited_left[i] = True
                    else:
                        continue

                end = queue_right.pop(0)
                a, b = self.get_coordinates(end)
                print("Node Explored from right", end, " ", "Its Coordinates are", a, ",", b, end=" ")
                print("It's neighbors are ", self.get_adjacent(end, self.dimension))

                #Right BFS Traversal from the ending node
                for j in self.get_adjacent(end, self.dimension):
                    if j not in self.Bi_BFS_dic_right.keys():
                        self.Bi_BFS_dic_right[j] = end

                    p, q = self.get_coordinates(j)
                    if self.array[p][q] == 1:
                        if self.BFS_visited_right[j] == False:
                            if self.BFS_visited_left[j] == True:

                                #Stop if left and right traversal intersects at a point
                                print("The search stops at intersection point ", j)
                                self.Bi_BFS_stop = j
                                self.Bi_BFS_dic_right[j] = end
                                return
                            else:
                                queue_right.append(j)
                                self.BFS_visited_right[j] = True
                    else:
                        continue


        #Function to get the append the path from the left and right traversal when they stop at an intersection point
        def get_Bi_BFS_path(self):
            path_left = []
            path_right = []

            if self.Bi_BFS_stop == 99:
                print("Path not possible")
            else:
                path_left.extend(self.get_path(self.Bi_BFS_stop, self.source, self.Bi_BFS_dic_left))
                path_left.append(self.source)
                path_left.reverse()
                path_right.extend(self.get_path(self.Bi_BFS_stop, self.destination, self.Bi_BFS_dic_right))
                path_right.pop(0)
                path_right.append(self.destination)
                self.path_Bi_BFS = path_left + path_right
                print("\nThe Path through Bi-directional BFS from", self.source, "to", self.destination, "is",
                      self.path_Bi_BFS)
                self.print_path(self.path_Bi_BFS)

        #Function to get the path from the left and right traversal respectively and return it to the aboev function where it is appended
        def get_path(self, start, end, dic):
                    path = []
                    while (start != end):
                        path.append(start)
                        if start in dic.keys():
                            start = dic[start]
                        else:
                            return
                    return path


        #This function prints the maze and indicates the path in red colour. It takes 
        def print_path(self, list):
                    for d in range(0, self.dimension):
                        for f in range(0, self.dimension):
                            if (d * self.dimension + f) in list:
                                print(colored(self.array[d][f], 'red'), end="\t")
                            else:
                                print(self.array[d][f], end="\t")
                        #                     print('\'%s\'' % self.array[d][f], end="\t")

                        print("")


        #Function to return a results array which contains to colour code for each cell of our maze and the path to be printed
        def colour_it(self, path, visited):
            temp = deepcopy(self.array)

            for q in range(self.dimension * self.dimension):
                if visited[q] == True:
                    c,d = self.get_coordinates(q)
                    temp[c][d]=3
            for p in path:
                a,b = self.get_coordinates(p)
                temp[a][b] = 4

            return temp

        #A seperate colour it function written for Bi-Directional BFS since it involves a 2 different colours for Left & Right traversal
        def colour_it_BiBFS(self, path, visited_L, visited_R):
            temp = deepcopy(self.array)

            for q in range(self.dimension * self.dimension):
                if visited_L[q] == True:
                    c,d = self.get_coordinates(q)
                    temp[c][d]=3
                if visited_R[q] == True:
                    l,m = self.get_coordinates(q)
                    temp[l][m]=8
            for p in path:
                a,b = self.get_coordinates(p)
                temp[a][b] = 4

            return temp
        
        #Function to Check if the Maze is solvable or Not
        def Solvable(self):
            self.BFS()
            self.DFS()
            if ((self.path_possible_BFS==1) and (self.path_possible_DFS==1)):
                return True
            else:
                return False
            
        #Function to return the performance of all the algorithms    
        def performance(self): 
            nodes_visited = {}
            path_length = {}
            self.Astar_Euc()
            self.Astar_Man()
            self.Bidirectional_BFS()
            
            #this is not to get stuck in infinte loop
            if ((self.Solvable()==True) and (self.path_possible_Man==1) and (self.path_possible_Euc==1)):
                #Count the number of cells visited by each of the algorithms
                nodes_visited['BFS']=self.BFS_visited.count(True)
                nodes_visited['DFS']=self.BFS_visited.count(True)
                nodes_visited['A-Star Euc']=self.Astar_visited_Euc.count(True)
                nodes_visited['A-Star Man']=self.Astar_visited_Man.count(True)
                nodes_visited['Bi-BFS']=self.BFS_visited_left.count(True)+ self.BFS_visited_right.count(True) -1
                
                #Length of the path returned by each of the algorithms
                path_length['BFS']=len(self.BFS_path)
                path_length['DFS']=len(self.BFS_path)
                path_length['A-Star Euc']=len(self.Astar_path_Euc)
                path_length['A-Star Man']=len(self.Astar_path_Man)
                path_length['Bi-BFS']=len(self.path_Bi_BFS)
                return nodes_visited, path_length
            
            else:
                if (self.stop_point<100):
                    self.stop_point+=1
                    self.performance()
                else:
                    self.stop_point=0
                    print("Maze is hard. Please change the P value")
                    return 
