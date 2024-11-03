from selenium import webdriver
import pandas as pd 
from bs4 import BeautifulSoup 
import time


# instantiate options for Chrome 
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument("--headless=new") 

# instantiate Chrome Webdriver 
driver = webdriver.Chrome(options=options)


# create data frame to save datas 
idx = 0
df = pd.DataFrame(columns=['Player', 'Nation', 'From', 'To', 'Price']) 
 

URL = 'https://www.footballtransfers.com/us/transfers/confirmed/2023-2024/uk-premier-league/' 
LIMIT = 18 
pages = []

for num in range(1, LIMIT + 1):
    driver.get(URL + str(num)) 

    page = driver.page_source
    pages.append(page) 
    # print(num) 
    time.sleep(1)
    
    
for i, page in enumerate(pages):
    soup = BeautifulSoup(page, 'html.parser')
    
    table = soup.find('tbody', id='player-table-body')
    rows = table.find_all('tr') 
    
    for row in rows:
        # tag td 
        nation = row.find('figure', class_='small-icon-image').find('img')
        date = row.find('td', class_="td-date d-none d-lg-table-cell").text 
        # print(nation.attrs)
        player = row.find('td', class_='td-player').find('span').text
        divs = row.find('td', class_='td-transfer').find_all('div', class_='transfer-club__name')

        price = row.find('td', class_='text-right td-price td-price--no-tag').find('span').text
        try:
            
            nation = nation.attrs['alt']
            fromm = divs[0].text
            too = divs[-1].text
            
            df.loc[idx] = [player, nation, fromm, too, (0.0 if price == 'Free' else float(price[1:len(price)-1]))]
            idx += 1
        except (AttributeError, IndexError):
            pass

df.to_csv('data.csv', index=False) 