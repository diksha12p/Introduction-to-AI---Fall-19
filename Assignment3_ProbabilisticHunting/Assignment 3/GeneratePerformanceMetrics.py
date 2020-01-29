# Importing modules
import AnalysisForEnvironment
import Agent
import MobileAgent

import pandas as pd

# Variables
FLAT_TERRAIN = 1
HILLY_TERRAIN = 2
FOREST_TERRAIN = 3
CAVE_TERRAIN = 4

terrain_type = [FLAT_TERRAIN, HILLY_TERRAIN, FOREST_TERRAIN, CAVE_TERRAIN]

data_rule_1 = []
data_rule_2 = []
data_rule_1_mobile = []
data_rule_2_mobile = []


# Rule 1 Implementation
for cell_type in terrain_type:
    for i in range(100):
        env = AnalysisForEnvironment.Environment(50, cell_type)
        agent = Agent.Agent(env, 1, 50)
        data_rule_1.append([cell_type, agent.final_steps])
        print("Iteration Number : {}".format(i))

df_rule_1 = pd.DataFrame(data_rule_1, columns=["Terrain Type", "Number Of Steps"])
df_rule_1.to_csv("Rule1_Data.csv", sep=',', encoding='utf-8', mode='a')


# Rule 2 Implementation
for cell_type in terrain_type:
    for i in range(100):
        env = AnalysisForEnvironment.Environment(50, cell_type)
        agent = Agent.Agent(env, 2, 50)
        data_rule_2.append([cell_type, agent.final_steps])
        print("Iteration Number : {}".format(i))

df_rule_2 = pd.DataFrame(data_rule_1, columns=["Terrain Type", "Number Of Steps"])
df_rule_2.to_csv("Rule2_Data.csv", sep=',', encoding='utf-8', mode='a')


# Rule 1 Implementation for Mobile Agent
for cell_type in terrain_type:
    for i in range(100):
        env = AnalysisForEnvironment.Environment(50, cell_type)
        agent = MobileAgent.Agent(env, 1, 50)
        data_rule_1_mobile.append([cell_type, agent.final_steps])
        print("Iteration Number : {}".format(i))

df_rule_1_mobile = pd.DataFrame(data_rule_1_mobile, columns=["Terrain Type", "Number Of Steps"])
df_rule_1_mobile.to_csv("Rule1_MobileAgent_Data.csv", sep=',', encoding='utf-8', mode='a')


# Rule 2 Implementation for Mobile Agent
for cell_type in terrain_type:
    for i in range(100):
        env = AnalysisForEnvironment.Environment(50, cell_type)
        agent = Agent.Agent(env, 2, 50)
        data_rule_2_mobile.append([cell_type, agent.final_steps])
        print("Iteration Number : {}".format(i))

df_rule_2_mobile = pd.DataFrame(data_rule_2_mobile, columns=["Terrain Type", "Number Of Steps"])
df_rule_2_mobile.to_csv("Rule2_MobileAgent_Data.csv", sep=',', encoding='utf-8', mode='a')