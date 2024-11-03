import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt

table = pd.read_csv('../part1/results.csv')
teams = table['Squad'].unique()


for team in teams: 
    stats = table[table['Squad'] == team].drop(columns=['Player', 'Nation', 'Pos', 'Squad'])  
    print(team) 
    for column in stats.columns: 
        data = stats[column].dropna(axis=0) 

        _, bins_edges, __ = plt.hist(data, edgecolor='black') 
        plt.ylabel('Number of players') 
        plt.xlabel(column.replace('_', ' ')) 
        plt.xticks(bins_edges, rotation=45) 
        column = column.replace("/", "_divide_")
        plt.savefig(f"../../images/teams/{team} {column}.png")
        plt.clf()