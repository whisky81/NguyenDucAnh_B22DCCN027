import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import argparse 


# example: python radarChartPlot.py  --p1 "Aaron Cresswell" --p2 "Aaron Ramsdale" --Attribute ""

# initialize parser 
parser = argparse.ArgumentParser()

parser.add_argument("--p1", required=True, type=str, help="Name of player 1")
parser.add_argument("--p2", required=True, type=str, help="Name of player 2")
parser.add_argument("--Attribute", required=True, type=str, help="Attributes that i want to use in radar plot")

# Example: python3 radarChartPlot.py  --p1 "Aaron Cresswell" --p2 "Aaron Ramsdale" --Attribute "Playing_Time_MP,Playing_Time_Starts,Playing_Time_Min"
agrs = parser.parse_args()
player1 = agrs.p1 
player2 = agrs.p2 
attrs = agrs.Attribute.split(",")


# load dataset 
df = pd.read_csv("../part1/results.csv") 


# transform attributes in attrs into a consistent scale 
# new scale 
new_max = 10
new_min = 0 
new_range = new_max - new_min 

# do a linear transformation on each variable to change value to "new_range"
for attr in attrs:
    max_val = df[attr].max()
    min_val = df[attr].min() 
    val_range = max_val - min_val
    
    df[attr] = df[attr].apply(lambda x: (((x - min_val) * new_range) / val_range) + new_min) 


df = df[df['Player'].isin([player1, player2])]
df = df[['Player'] + attrs] 



import plotly.graph_objects as go 

fig = go.Figure() 

player1_values = df.loc[0].tolist()
# print(player1_values)

fig.add_trace(go.Scatterpolar(
    r = player1_values[1:],
    theta = attrs,
    fill = 'toself',
    name = player1_values[0]
))


player2_values = df.loc[1].tolist()
fig.add_trace(go.Scatterpolar(
    r = player2_values[1:],
    theta = attrs,
    fill = 'toself',
    name = player2_values[0]
))

fig.update_layout(
    polar = dict(
        radialaxis=dict(
        visible=True,
        range=[0, new_max]
    )),
    showlegend=False
)

fig.show()