import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from bs4 import BeautifulSoup
import pandas as pd
import json
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from datetime import datetime
import psycopg2

#api links 
SA_url = 'https://qzlsklfacc.medianetwork.cloud/get_nft?collection=meerkatmillionairescc&page=0&limit=9999&order=price-ASC&fits=any&trait=&search=&min=0&max=0&listed=true&ownedby=&attrib_count=&bid=all'
DE_url = 'https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=Meerkat%20Millionaires%20Country%20Club'
ME_url = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22meerkat_millionaires_country_club%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%2C%22createdAt%22%3A-1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A10000%7D'
SS_url = 'https://solsea.io/collection/6151ef66fe4a0643c2ae0710'

#intialize dataframe
global df
df = pd.DataFrame()

#Solanart data
def SA_scrape(URL):
    global df
    page = requests.get(URL).json()
    maxpage = page['pagination']['maxPages']

    for test in range(0,maxpage+1):
        URL = 'https://qzlsklfacc.medianetwork.cloud/get_nft?collection=meerkatmillionairescc&page={}&limit=9999&order=price-ASC&fits=any&trait=&search=&min=0&max=0&listed=true&ownedby=&attrib_count=&bid=all'.format(test)
        page = requests.get(URL).json()

        for item in page['items']:
            price = item['price']

            row = pd.DataFrame(data = [price, "Solanart"]).T
            df = df.append(row)

#Digitaleyes data
def DE_scrape(URL):
    try:
        global df
        page = requests.get(URL).json()
        next_curs = page['next_cursor']
        
        for item in page['offers']:
            price = item['price']/1000000000

            row = pd.DataFrame(data = [price, "Digitaleyes"]).T
            df = df.append(row)
        if next_curs != None:
            next_URL = DE_url + '&cursor=' + next_curs  
            return DE_scrape(next_URL)
        else:
            pass
    except:
        print("DE Error DB script")

#Magic Eden data
def ME_scrape(URL):
    try:
        global df
        page = requests.get(URL).json()
        for item in page['results']:
            price = item['price']

            row = pd.DataFrame(data = [price, "Magic Eden"]).T
            df = df.append(row)
    except:
        print("ME Error")    

def Holders():
    try:
        global holder
        TURL = 'https://howrare.is/meerkatmillionaires/owners'
        page = requests.get(TURL,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'})
        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all("td")
        holder = items[1].text
    except:
        holder = 0

#run data scrapes
SA_scrape(SA_url)
DE_scrape(DE_url)
ME_scrape(ME_url)
Holders()


#format dataframe
df.columns = ["Price","Market"]
df.sort_values(by = ['Price'], inplace=True)

#find floors
try:
    SA_floor = min(df.loc[df['Market'] == 'Solanart', 'Price'])
except:
    SA_floor = "Error"
try:    
    DE_floor = min(df.loc[df['Market'] == 'Digitaleyes', 'Price'])
except:
    DE_floor = "Error"
try:
    ME_floor = min(df.loc[df['Market'] == 'Magic Eden', 'Price'])
except:
    ME_floor = "Error"


con = psycopg2.connect(
        host = "ec2-35-153-88-219.compute-1.amazonaws.com",
        database = "d8moers639v8ep",
        user = "rtqdsyhnkwqepo",
        password = "9756e62250ffd60cbd98b664fc857623393385145d7fd429c67b9186b94d5afc"
)

cur = con.cursor()
ins_script = "INSERT INTO floor (date, SA, DE, ME, listed, holder) VALUES (%s,%s,%s,%s,%s,%s)"
ins_value = (datetime.now(),SA_floor,DE_floor,ME_floor,len(df),int(holder))
cur.execute(ins_script,ins_value) 
con.commit()
con.close()
print("DB complete")

