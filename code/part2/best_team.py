import pandas as pd

df = pd.read_csv('../part1/results.csv')


columns_to_sum = df.columns[5:].tolist()
df[columns_to_sum] = df[columns_to_sum].apply(pd.to_numeric, errors='coerce')


team_stats = df.groupby('Squad')[columns_to_sum].sum()


highest_team_stats = team_stats.idxmax()
highest_team_stats.to_csv('best_squad.csv')
print(highest_team_stats.value_counts())
