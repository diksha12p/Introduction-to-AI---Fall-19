# Q 2.3 
#Given DIM -> Solvability vs P

import matplotlib.pyplot as plt
import pandas as pd

def Probability(d):
    s= {}
    for p in np.arange(0.1,0.9,0.1):
        solve=0
        for i in range(1,100):
            M=Maze(p,d)
            M.Mazeinitialise()
            if (M.Solvable()==True):
                solve+=1
        s[p.round(decimals=2)]=solve/100
    return s

M = {}
for d in range(5,50,5):
    s=Probability(d)
    M[d]= s


df=pd.DataFrame(M)
df.index.name = 'Maze Probability'
df.columns.name="Dimension"
df
df.plot()

#Question 2.1


#Question 2.1


import time

# Below function generates a solvable maze and return if it gets a Solvable Maze in 10 iterations
def generate_solvable(p,d,stop):
    N=Maze(p,d)
    N.Mazeinitialise()
    if (N.Solvable()==True):
        return N
    else:
        if (stop<=10):
            stop+=1
            generate_solvable(p, d, stop)
        else:
            return False
        
        
        
#Getting the average time taken for DFS for a range of P X D values - Average of 20 Solvable Matrices
stat={}
all={}
for d in range (3,15):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        t2=[]
        for i in range(0,20):
            N=generate_solvable(p, d, 0)
            if (N!=None):
                t1=time.time()
                N.DFS()
                t2.append((time.time()-t1))
        stat[p]=sum(t2)/len(t2)
    all[d]=stat
    stat={}
        


import pandas as pd
DFS_time=pd.DataFrame(all).transpose()
DFS_time.index.name = 'Dimension'
DFS_time.columns.name="P-value of the Maze"

        
#Getting the average time taken for BFS for a range of P X D values - Average of 20 Solvable Matrices
stat={}
all_DFS={}
for d in range (3,15):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        t2=[]
        for i in range(0,20):
            N=generate_solvable(p, d, 0)
            if (N!=None):
                t1=time.time()
                N.DFS()
                t2.append((time.time()-t1))
        stat[p]=sum(t2)/len(t2)
    all_DFS[d]=stat
    stat={}
    
import pandas as pd
BFS_time=pd.DataFrame(all_DFS).transpose()
BFS_time.index.name = 'Dimension'
BFS_time.columns.name="P-value of the Maze"
    
    
#Getting the average time taken for Bi-BFS for a range of P X D values - Average of 20 Solvable Matrices
stat={}
all_Bi_BFS={}
for d in range (3,15):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        t2=[]
        for i in range(0,20):
            N=generate_solvable(p, d, 0)
            if (N!=None):
                t1=time.time()
                N.DFS()
                t2.append((time.time()-t1))
        stat[p]=sum(t2)/len(t2)
    all_Bi_BFS[d]=stat
    stat={}
    
Bi_BFS_time=pd.DataFrame(all).transpose()
Bi_BFS_time.index.name = 'Dimension'
Bi_BFS_time.columns.name="P-value of the Maze"


   # Below function generates a solvable maze and return if it gets a Solvable Maze in 10 iterations
def generate_solvable_Astar(p, d, stop):
    N=Maze(p,d)
    N.Mazeinitialise()
    N.Astar_Euc()
    N.Astar_Man()
    if ((N.Solvable()==True) and (N.path_possible_Man==1) and (N.path_possible_Euc==1)):
        return N
    else:
        if (stop<=30):
            stop+=1
            generate_solvable_Astar(p, d, stop)
        else:
            return None
        
#Path Length - A-Star Euclidean VS A-star Manhattan
length_Euc={}
Path_length_Euc={}
length_Man={}
Path_length_Man={}
for d in range (3, 5):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        l_euc=[]
        l_man=[]
        for i in range(0,20):
            N=generate_solvable_Astar(p, d, 0)
            if (N!=None):
                b_e = len(N.Astar_path_Euc)
                b_m = len(N.Astar_path_Man)
                l_euc.append(b_e)
                l_man.append(b_m)
        if (len(l_euc)!=0):
            length_Euc[p]=sum(l_euc)/len(l_euc)
        else:
            length_Euc[p]=0
            
        if (len(l_man)!=0):
            length_Man[p]=sum(l_man)/len(l_man)
        else:
            length_Man[p]=0
    Path_length_Euc[d]=length_Euc
    Path_length_Man[d]=length_Man
    length_Euc={}
    length_Man={}
    
    
import pandas as pd
Path_length_Euc= pd.DataFrame(Path_length_Euc)
Path_length_Man= pd.DataFrame(Path_length_Euc)


#Node Visted - A-Star Euclidean VS A-star Manhattan
c_Euc={}
nodes_Euc={}

c_Man={}
nodes_Man={}
for d in range (3, 5):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        l_euc=[]
        l_man=[]
        for i in range(0,20):
            N=generate_solvable_Astar(p, d, 0)
            if (N!=None):
                b_e = N.Astar_visited_Euc.count(True)
                b_m = N.Astar_visited_Man.count(True)
                l_euc.append(b_e)
                l_man.append(b_m)
        if (len(l_euc)!=0):
            c_Euc[p]=sum(l_euc)/len(l_euc)
        else:
            c_Euc[p]=0
            
        if (len(l_man)!=0):
            c_Man[p]=sum(l_man)/len(l_man)
        else:
            c_Man[p]=0
    nodes_Euc[d]=c_Euc
    nodes_Man[d]=c_Man
    c_Euc={}
    c_Man={}
    
    
nodes_Euc= pd.DataFrame(nodes_Euc)
nodes_Man= pd.DataFrame(nodes_Man)

#Time taken - A-Star Euclidean VS A-star Manhattan
import time
stat={}
Euc_time={}
for d in range (5, 60, 5):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        t2=[]
        for i in range(0,20):
            N=generate_solvable_Astar(p, d, 0)
            if (N!=None):
                t1=time.time()
                N.Astar_Euc()
                t2.append((time.time()-t1))
        if (len(t2)!=0):
            stat[p]=sum(t2)/len(t2)
        else:
            stat[p]=0
    Euc_time[d]=stat
    stat={}
    
Euc_time=pd.DataFrame(Euc_time).transpose()
Euc_time.index.name = 'Dimension'
Euc_time.columns.name="P-value of the Maze"
Euc_time=Euc_time*1000

import time
stat={}
Man_time={}
for d in range (5, 60, 5):
    pr= np.arange(0.1, 0.5, 0.1)
    for p in pr.round(decimals=2):
        t2=[]
        for i in range(0,20):
            N=generate_solvable_Astar(p, d, 0)
            if (N!=None):
                t1=time.time()
                N.Astar_Man()
                t2.append((time.time()-t1))
        if (len(t2)!=0):
            stat[p]=sum(t2)/len(t2)
        else:
            stat[p]=0
    Man_time[d]=stat
    stat={}
    
Man_time=pd.DataFrame(Man_time).transpose()
Man_time.index.name = 'Dimension'
Man_time.columns.name="P-value of the Maze"
Man_time=Man_time*1000