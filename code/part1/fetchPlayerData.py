import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment 
import pandas as pd  
import numpy as np

def get_table(
    url: str
):
    page = requests.get(url) 
    soup = BS(page.text, 'html.parser') 

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))  

    comment_soup = BS(comments[28], 'html.parser') 

    table = comment_soup.find('table')

    # handling headers 
    thead = table.find('thead')  

    rows = thead.find_all('tr') 

    prefixs = [] 
    heads = rows[0].find_all('th') 
    for head in heads:
        if num := head.get('colspan'):
            content = head.text.replace(' ', '_') 
            prefixs.append((int(num), content)) 

    prefixs.append((1, '')) 

    columns = [] 
    heads = rows[-1].find_all('th') 

    i = 0 
    for num, prefix in prefixs:
        for j in range(i, i + num):
            field = prefix + ('' if prefix == '' else '_') + heads[j].text.replace(' ', '')
            columns.append(field)
        i += num 

    df = pd.DataFrame(columns=columns[1:])   

    # handling body
    tbody = table.find('tbody') 

    rows = tbody.find_all('tr') 
    i = 0 

    for row in rows:
        datas = row.find_all('td') 
        if len(datas) != 0:
            datas = [data.text for data in datas] 
            df.loc[i] = datas 
            i += 1

    return df


tables = [] 
urls = [
    'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats',
    'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats',
    'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats',
    'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats',
    'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats',  
    'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats', 
    'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats', 
    'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats', 
    'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats',
    'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
]

for i, url in enumerate(urls):
    print(i)
    table = get_table(url)  
    tables.append(table)


columns = [
	['stats', ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Playing_Time_MP',
       'Playing_Time_Starts', 'Playing_Time_Min',
       'Performance_Ast',
       'Performance_G-PK', 'Performance_PK',
       'Performance_CrdY', 'Performance_CrdR', 'Expected_xG', 'Expected_npxG',
       'Expected_xAG','Progression_PrgC',
       'Progression_PrgP', 'Progression_PrgR', 'Per_90_Minutes_Gls',
       'Per_90_Minutes_Ast', 'Per_90_Minutes_G+A', 'Per_90_Minutes_G-PK',
       'Per_90_Minutes_G+A-PK', 'Per_90_Minutes_xG', 'Per_90_Minutes_xAG',
       'Per_90_Minutes_xG+xAG', 'Per_90_Minutes_npxG',
       'Per_90_Minutes_npxG+xAG']],
    ['keepers', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Performance_GA', 'Performance_GA90', 'Performance_SoTA',
       'Performance_Saves', 'Performance_Save%', 'Performance_W',
       'Performance_D', 'Performance_L', 'Performance_CS', 'Performance_CS%',
       'Penalty_Kicks_PKatt', 'Penalty_Kicks_PKA', 'Penalty_Kicks_PKsv',
       'Penalty_Kicks_PKm', 'Penalty_Kicks_Save%']],
    ['shooting', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Standard_Gls', 'Standard_Sh', 'Standard_SoT', 'Standard_SoT%',
       'Standard_Sh/90', 'Standard_SoT/90', 'Standard_G/Sh', 'Standard_G/SoT',
       'Standard_Dist', 'Standard_FK', 'Standard_PK', 'Standard_PKatt',
       'Expected_xG', 'Expected_npxG', 'Expected_npxG/Sh', 'Expected_G-xG',
       'Expected_np:G-xG']],
    ['passing', ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Total_Cmp',
       'Total_Att', 'Total_Cmp%', 'Total_TotDist', 'Total_PrgDist',
       'Short_Cmp', 'Short_Att', 'Short_Cmp%', 'Medium_Cmp', 'Medium_Att',
       'Medium_Cmp%', 'Long_Cmp', 'Long_Att', 'Long_Cmp%', 'Ast', 'xAG',
       'Expected_xA', 'Expected_A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP']],
    ['passingtype', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Pass_Types_Live', 'Pass_Types_Dead', 'Pass_Types_FK', 'Pass_Types_TB',
       'Pass_Types_Sw', 'Pass_Types_Crs', 'Pass_Types_TI', 'Pass_Types_CK',
       'Corner_Kicks_In', 'Corner_Kicks_Out', 'Corner_Kicks_Str',
       'Outcomes_Cmp', 'Outcomes_Off', 'Outcomes_Blocks']],
    ['gca', ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'SCA_SCA',
       'SCA_SCA90', 'SCA_Types_PassLive', 'SCA_Types_PassDead', 'SCA_Types_TO',
       'SCA_Types_Sh', 'SCA_Types_Fld', 'SCA_Types_Def', 'GCA_GCA',
       'GCA_GCA90', 'GCA_Types_PassLive', 'GCA_Types_PassDead', 'GCA_Types_TO',
       'GCA_Types_Sh', 'GCA_Types_Fld', 'GCA_Types_Def']],
    ['defense', ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Tackles_Tkl',
       'Tackles_TklW', 'Tackles_Def3rd', 'Tackles_Mid3rd', 'Tackles_Att3rd',
       'Challenges_Tkl', 'Challenges_Att', 'Challenges_Tkl%',
       'Challenges_Lost', 'Blocks_Blocks', 'Blocks_Sh', 'Blocks_Pass', 'Int',
       'Tkl+Int', 'Clr', 'Err']], 
    ['possession', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Touches_Touches', 'Touches_DefPen', 'Touches_Def3rd', 'Touches_Mid3rd',
       'Touches_Att3rd', 'Touches_AttPen', 'Touches_Live', 'Take-Ons_Att',
       'Take-Ons_Succ', 'Take-Ons_Succ%', 'Take-Ons_Tkld', 'Take-Ons_Tkld%',
       'Carries_Carries', 'Carries_TotDist', 'Carries_PrgDist', 'Carries_PrgC',
       'Carries_1/3', 'Carries_CPA', 'Carries_Mis', 'Carries_Dis',
       'Receiving_Rec', 'Receiving_PrgR']],
    ['playingtime', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Starts_Starts', 'Starts_Mn/Start', 'Starts_Compl',
       'Subs_Subs', 'Subs_Mn/Sub', 'Subs_unSub', 'Team_Success_PPM',
       'Team_Success_onG', 'Team_Success_onGA',
       'Team_Success_(xG)_onxG',
       'Team_Success_(xG)_onxGA']],
    ['misc', ['Player', 'Nation', 'Pos', 'Squad', 'Age',
       'Performance_Fls', 'Performance_Fld', 'Performance_Off',
       'Performance_Crs',
		'Performance_OG',
       'Performance_Recov', 'Aerial_Duels_Won', 'Aerial_Duels_Lost',
       'Aerial_Duels_Won%']]
]


for i, table in enumerate(tables): 
    new_table = table.filter(items=columns[i][1], axis=1)  
    tables[i] = new_table

common_columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age'] 

results = tables[0] 

for i in range(1, len(tables)):  
    results = results.merge(tables[i], how = 'outer', on = common_columns)   
    

df = results.copy() 
df = df.convert_dtypes() 
df.info() 
df['Playing_Time_Min'] = df['Playing_Time_Min'].str.replace(',', '').astype('Int64')

for column in df.columns[4:]: 
    df[column] = pd.to_numeric(df[column], errors='coerce')   


df = df[df['Playing_Time_Min'] > 90]   
df['firstname'] = df['Player'].str.split().str[0].astype('string')

df_sorted = df.sort_values(by=['firstname', 'Age'], ascending=[True, False]) 

df_sorted.drop('firstname', axis=1, inplace=True) 
df_sorted.to_csv('results.csv', index=False)