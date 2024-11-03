# %%
import pandas as pd  
import numpy as np

table = pd.read_csv('../part1/results.csv') 


# %%
fields = [''] 
row = ['all']

for column in table.columns[4:]:  
    table.sort_values(by=column, ascending=False, inplace=True)   

    datas = table.dropna(axis=0, subset=[column]) 
       
    print(datas.head(3).get(['Player', 'Nation', 'Pos', 'Squad', column])) 
    print(datas.tail(3)[::-1].get(['Player', 'Nation', 'Pos', 'Squad', column]))    

    fields.append(f"Median of {column}") 
    fields.append(f"Mean of {column}") 
    fields.append(f"Std of {column}")  
    
    arr = np.array(table[column].dropna())    

    row.append(np.median(arr))
    row.append(np.mean(arr))
    row.append(np.std(arr))

    

# %%
df = pd.DataFrame(columns=fields) 

# %%
df.loc[len(df)] = row

teams = table['Squad'].unique()


# %%
rows = [[f"{team}"] for team in teams]

for i, team in enumerate(teams):  
    stats = table[table['Squad'] == team].drop(columns=['Player', 'Nation', 'Pos', 'Squad']) 
    medians = stats.median().to_list() 
    means = stats.mean().to_list() 
    stds = stats.std().to_list()  

    for j in range(len(medians)): 
        rows[i].append(medians[j]) 
        rows[i].append(means[j]) 
        rows[i].append(stds[j]) 
    

# %%
for row in rows: 
    df.loc[len(df)] = row

# %%
df.to_csv('results2.csv')