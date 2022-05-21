import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from bs4 import BeautifulSoup
import pandas as pd
import json
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from datetime import datetime


def app():

    #api links 
    SA_url = 'https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=nakedmeerkatsbeachclub'
    DE_url = 'https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=Naked%20Meerkats%20Beach%20Club'
    ME_url = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22naked_meerkats_beach_club%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%2C%22createdAt%22%3A-1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A10000%7D'
    SS_url = 'https://solsea.io/collection/6151ef66fe4a0643c2ae0710'


    #rank data scraped from howrare.is
    global ranks
    ranks = pd.read_csv('NMBC_ranks.csv')

    #load attribute data
    q = open('nmbc_atts.json')
    atts_json = json.load(q)
    attributes = atts_json['Attributes']

    #intialize dataframe
    global df
    df = pd.DataFrame()

    #Solanart data
    def SA_scrape(URL):
        global df
        global ranks
        page = requests.get(URL).json()

        for item in page:
            price = item['price']
            id = item['name'].split('#')[1]
            seller = 'https://solscan.io/account/' + item['seller_address']
            buylink = 'https://solanart.io/search/?token=' + item['token_add']
            img = item['link_img']
            atts = item['attributes'].split(",")
            background = atts[0].split(": ")[1]
            fur = atts[1].split(": ")[1]
            eyes = atts[2].split(": ")[1]
            hair = atts[3].split(": ")[1]
            mouth = atts[4].split(": ")[1]
            try:
                necklace = atts[5].split(":")[1]
            except:
                necklace = 'None'
            howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
            moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()
    
            row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Solanart", buylink, img, background, fur, eyes, hair, mouth, necklace]).T
            df = df.append(row)

    #Digitaleyes data
    def DE_scrape(URL):
        try:
            global df
            global ranks
            page = requests.get(URL).json()
            next_curs = page['next_cursor']
            
            for item in page['offers']:
                price = item['price']/1000000000
                id = item['metadata']['name'].split('#')[1]
                seller = 'https://solscan.io/account/' + item['owner']
                buylink = 'https://digitaleyes.market/item/' + item['mint']
                img = item['metadata']['image']
                atts = item['metadata']['attributes']
                background = atts[0]['value']
                fur = atts[1]['value']
                eyes = atts[2]['value']
                hair= atts[3]['value']
                mouth = atts[4]['value']
                necklace = atts[5]['value']
                howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()

                row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Digitaleyes", buylink, img, background, fur, eyes, hair, mouth, necklace]).T
                df = df.append(row)
            if next_curs != None:
                next_URL = DE_url + '&cursor=' + next_curs + '%3D%3D&price=asc'   
                return DE_scrape(next_URL)
            else:
                pass
        except:
            print("DE Error")
    
    #Magic Eden data
    def ME_scrape(URL):
        try:
            global df
            global ranks
            page = requests.get(URL).json()
            for item in page['results']:
                price = item['price']
                id = item['title'].split('#')[1]
                seller = 'https://solscan.io/account/' + item['owner']
                buylink = 'https://www.magiceden.io/item-details/' + item['mintAddress']
                img = item['img']
                atts = item['attributes']
                background = atts[0]['value']
                fur = atts[1]['value']
                eyes = atts[2]['value']
                hair= atts[3]['value']
                mouth = atts[4]['value']
                necklace = atts[5]['value']
                howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()

                row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Magic Eden", buylink, img, background, fur, eyes, hair, mouth, necklace]).T
                df = df.append(row)
        except:
            print("ME Error")  

    #Solsea data
    def SS_scrape(URL):
        try:
            global SS_floor
            SS_page = requests.get(URL)
            SS_soup = BeautifulSoup(SS_page.text,'html.parser')
            SS_temp = SS_soup.find_all("h4", {"class":"price-floor__CollectionPage_KW6R2"})
            SS_floor = float(SS_temp[1].find_all("span")[0].text.split(" ")[0])
        except:
            SS_floor = "Error"  

    #AA data
    def AA_scrape(token):
        try:
            global df
            page = requests.post("https://apis.alpha.art/api/v1/collection", json={"collectionId":"naked-meerkat","orderBy":"PRICE_LOW_TO_HIGH","status":["BUY_NOW"],"token":token}).json()
            try:
                token = page['nextPage']
            except:
                token = 'None'
            
            for item in page['tokens']:
                id = item['title'].split('#')[1]
                price = int(item['price'])/1000000000
                buylink = 'https://alpha.art/t/' + item['mintId']
                howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()

                resp = requests.get('https://apis.alpha.art/api/v1/token/' + item['mintId']).json()
                img = resp['token']['image']
                seller = 'https://solscan.io/account/' + resp['token']['currentOwner']
                atts = resp['token']['metadata']['attributes']
                background = atts[0]['value']
                fur = atts[1]['value']
                eyes = atts[2]['value']
                hair= atts[3]['value']
                mouth = atts[4]['value']
                necklace = atts[5]['value']

                row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Alpha Art", buylink, img, background, fur, eyes, hair, mouth, necklace]).T
                df = df.append(row)
            if token != 'None':  
                return AA_scrape(token)
            else:
                pass 
        except:
            print("AA Error")  

    #run data scrapes
    SA_scrape(SA_url)
    DE_scrape(DE_url)
    ME_scrape(ME_url)
    SS_scrape(SS_url)
    AA_scrape('')

    #format dataframe
    df.columns = ["Price","Rank","MoonRank","ID","Seller Wallet","Market","Listing Link","Image","Background","Fur","Eyes","Hair","Mouth","Necklace"]
    df.Rank = pd.to_numeric(df.Rank, errors = 'coerce')
    df.sort_values(by = ['Price'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.replace({'null' : 'None'}, regex=True)

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
    try:
        AA_floor = min(df.loc[df['Market'] == 'Alpha Art', 'Price'])
    except:
        AA_floor = "Error"
    SS_floor = "N/A"  

    #Side bar data
    st.sidebar.title("Attribute Filters")

    rank_type = st.sidebar.selectbox('Ranking Filtering Method:', ['MoonRank','Howrare.is'])

    rank_choice = st.sidebar.number_input('Max Meerkat Rank:', min_value = 1, max_value = 10031, step = 1, value = 10031)
    if rank_type == 'Howrare.is':
        df = df[df['Rank'] <= rank_choice]
    else:
        df = df[df['MoonRank'] <= rank_choice]

    market_choice = st.sidebar.selectbox('Market:', ['All', 'Solanart','Alpha Art','Magic Eden','Digital Eyes'])
    if market_choice != 'All':
        df = df[df['Market']  == market_choice]

    background_choice = st.sidebar.selectbox('Background:', attributes['Background'])
    if background_choice != 'All':
        df = df[df['Background']  == background_choice.split(" (")[0]]

    fur_choice = st.sidebar.selectbox('Fur:', attributes['Fur'])
    if fur_choice != 'All':
        df = df[df['Fur']  == fur_choice.split(" (")[0]]

    eyes_choice = st.sidebar.selectbox('Eyes:', attributes['Eyes'])
    if eyes_choice != 'All':
        df = df[df['Eyes']  == eyes_choice.split(" (")[0]]

    hair_choice = st.sidebar.selectbox('Hair:', attributes['Hair'])
    if hair_choice != 'All':
        df = df[df['Hair']  == hair_choice.split(" (")[0]]

    mouth_choice = st.sidebar.selectbox('Mouth:', attributes['Mouth'])
    if mouth_choice != 'All':
        df = df[df['Mouth']  == mouth_choice.split(" (")[0]]

    necklace_choice = st.sidebar.selectbox('Necklace:', attributes['Necklace'])
    if necklace_choice != 'All':
        df = df[df['Necklace']  == necklace_choice.split(" (")[0]]


    #Streamlit commands
    st.subheader("NMBC Market Floor Prices")
    st.write("**Note:** This may be slighty out of sync with the blockchain")
    s2 = pd.Series([SA_floor, AA_floor, DE_floor, ME_floor, SS_floor])
    Frame2 = pd.DataFrame(data = [list(s2)], index = ["Floor Price"], columns = ["Solanart", "Alpha Art","Digitaleyes","Magic Eden","Solsea"])
    Frame2.style.set_properties(**{'text-align': 'left'})
    st.table(Frame2)

    st.subheader("Current NMBC Market Listings")
    st.write("Data from Solanart, Alpha Art, Magic Eden, and Digital Eyes")

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()

    link_jscode = JsCode("""
    function(params) {
        var element = document.createElement("span");
        var linkElement = document.createElement("a");
        var linkText = document.createTextNode('Link');
        link_url = params.value;
        linkElement.appendChild(linkText);
        linkText.title = 'Link';
        linkElement.href = link_url;
        linkElement.target = "_blank";
        element.appendChild(linkElement);
        return element;
    };
    """)

    sol_jscode = JsCode("""
    function(params) {
        var element = document.createElement("span");
        var linkElement = document.createElement("a");
        var linkText = document.createTextNode('Solscan');
        link_url = params.value;
        linkElement.appendChild(linkText);
        linkText.title = 'Solscan';
        linkElement.href = link_url;
        linkElement.target = "_blank";
        element.appendChild(linkElement);
        return element;
    };
    """)

    img_jscode = JsCode("""
    function(params) {
        var element = document.createElement("span");
        var linkElement = document.createElement("a");
        var linkText = document.createTextNode('Arweave');
        link_url = params.value;
        linkElement.appendChild(linkText);
        linkText.title = 'Arweave';
        linkElement.href = link_url;
        linkElement.target = "_blank";
        element.appendChild(linkElement);
        return element;
    };
    """)

    gb.configure_column("Image", cellRenderer=img_jscode)
    gb.configure_column("Seller Wallet", cellRenderer=sol_jscode)
    gb.configure_column("Listing Link", cellRenderer=link_jscode)
    gridOptions = gb.build()
    AgGrid(df,allow_unsafe_jscode=True, theme="streamlit", gridOptions=gridOptions, fit_columns_on_grid_load=True)

    st.write("")

    def render_stacked_area_chart():
        cts = df['Price'].value_counts().sort_index().tolist()
        unique = list(df['Price'].value_counts().sort_index().keys())
        cum = df['Price'].value_counts().sort_index().cumsum().tolist()

        option = {
            "title": {
                "left": "center",
                "text": "Meerkat Order Book"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
            },
            "legend": {
                "data": ["For Sale", "Cumulative"],
                "top": 25
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
            "xAxis": [
                {
                    "name": "Price",
                    "type": "category",
                    "boundaryGap": False,
                    "data": unique,
                }
            ],
            "yAxis": [{"type": "value", "name":"# Meerkats"}],
            "dataZoom": [
                {
                    "type": 'inside',
                    "start": 0,
                    "end": 25
                },
                {
                    "start": 0,
                    "end": 25
                }
            ],
            "series": [
                {
                    "name": "For Sale",
                    "type": "line",
                    "data": cts,
                },
                {
                    "name": "Cumulative",
                    "type": "line",
                    "stack": "Total",
                    "areaStyle": {},
                    "emphasis": {"focus": "series"},
                    "data": cum,
                },
            ],
        }
        st_echarts(options=option, height="500px")

    render_stacked_area_chart()

    def render_scatter_chart():
        if rank_type == 'Howrare.is':
            datas = list(zip(df['Rank'],df['Price']))
        else:
            datas = list(zip(df['MoonRank'],df['Price']))

        option = {
            "title": {
                "left": "center",
                "text": "Meerkat Price vs. Rank"
                },
            "tooltip": {
                "trigger": "item",
                "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
            },
            "xAxis": {"name":"Rank","max": 10031},
            "yAxis": {"name":"Price","type":"log"},
            "dataZoom": [
                {
                    "type": 'inside',
                    "start": 0,
                    "end": 100
                },
                {
                    "start": 0,
                    "end": 100
                }
            ],
            "series": [
                {
                "symbolSize": 5,
                "data": datas,
                "type": 'scatter',
                "name": "Price"
                }
            ]
        }
        st_echarts(options=option, height="500px")

    render_scatter_chart()

    st.subheader("NMBC Whale Tracker as of 12-3-2021 2:00 AM UTC")

    c1, c2 = st.columns(2)
    with c1:
        whale = pd.read_csv('NMBC_whales.csv', index_col=False)
        gb2 = GridOptionsBuilder.from_dataframe(whale)
        gb2.configure_pagination()
        gb2.configure_column("Link", cellRenderer=sol_jscode)
        gb2.configure_column("NFTEyez Link", cellRenderer=link_jscode)
        gridOptions2 = gb2.build()
        grid_return1 = AgGrid(whale,allow_unsafe_jscode=True, theme="streamlit", gridOptions=gridOptions2, fit_columns_on_grid_load=True)


    with c2:
        chart = pd.read_csv('NMBC_chart.csv', index_col=False)
        def render_bar_chart():
            option = {
                "title": {
                "left": "center",
                "text": "Naked Meerkat Distribution per Wallet Size (4359 Holders)"
                },
                "tooltip": {
                    "trigger": 'axis',
                    "axisPointer": {
                    "type": 'shadow'
                    }
                },
                "legend": {"top": 25},
                "grid": {
                    "left": '3%',
                    "right": '4%',
                    "bottom": '3%',
                    "containLabel": "true"
                },
                "yAxis": {
                    "type": 'value',
                    "name": '# Meerkats'
                },
                "xAxis": {
                    "type": 'category',
                    "name": '# Owned',
                    "data": ['1', '2-4', '5-9', '10-19', '20-29', '30-49', '50-99', '100+']
                },
                "series": [
                    {
                    "name": 'Holding',
                    "type": 'bar',
                    "stack": 'total',
                    "label": {
                        "show": "true"
                    },
                    "data": chart['# Holding'].to_list()
                    },

                    {
                    "name": 'Listed',
                    "type": 'bar',
                    "stack": 'total',
                    "label": {
                        "show": "true"
                    },
                    "data": chart['# Listed'].to_list()
                    }
                ],
            }
            st_echarts(options=option, height="410px")
        
        grid_return2 = render_bar_chart()

    st.write("**Note:** This may break at any time, feel free to @JG#4765 in the Meerkat discord for help!")
    st_autorefresh(interval=2 * 60 * 1000, key="dataframerefresh")
