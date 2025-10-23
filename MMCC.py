import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import json
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from datetime import datetime
import psycopg2
import os

def app():

    #api links 
    reward_url = 'https://api.solscan.io/account?address=mmccxRQPmAt7yfK3fpEnW7mDtQYBMP7zgWaxohEzGm6'
    SA_url = 'https://api.solanart.io/get_nft?collection=meerkatmillionairescc&page=0&limit=9999&order=price-ASC&min=0&max=99999&search=&listed=true&fits=all&bid=all'
    #SA_url = 'https://qzlsklfacc.medianetwork.cloud/get_nft?collection=meerkatmillionairescc&page=0&limit=9999&order=price-ASC&fits=any&trait=&search=&min=0&max=0&listed=true&ownedby=&attrib_count=&bid=all'
    DE_url = 'https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=Meerkat%20Millionaires%20Country%20Club'
    ME_url = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22meerkat_millionaires_country_club%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%2C%22createdAt%22%3A-1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A9999%7D'


    #Reward pool
    reward_json = requests.get(reward_url,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}).json()
    reward_floor = reward_json['data']['lamports']/1000000000
    reward = reward_floor/10000
    reward_mint = reward*.15
    reward_hold = reward*.85

    date_1 = '9/5/2022 3:00:00'
    date_format_str = '%d/%m/%Y %H:%M:%S'
    start = datetime.strptime(date_1, date_format_str)
    end =   datetime.now()
    diff = end - start
    diff_in_hours = diff.total_seconds() / 3600
    estimate_both = (reward_floor/diff_in_hours)*24*7/9999
    estimate_hold = estimate_both*.85
    estimate_mint = estimate_both*.15


    #rank data scraped from howrare.is
    global ranks
    ranks = pd.read_csv('MMCC_ranks.csv')

    #load attribute data
    q = open('mmcc_atts.json')
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
        maxpage = page['pagination']['maxPages']

        for test in range(0,maxpage+1):
            #URL = 'https://qzlsklfacc.medianetwork.cloud/get_nft?collection=meerkatmillionairescc&page={}&limit=9999&order=price-ASC&fits=any&trait=&search=&min=0&max=0&listed=true&ownedby=&attrib_count=&bid=all'.format(test)
            URL = 'https://api.solanart.io/get_nft?collection=meerkatmillionairescc&page={}&limit=9999&order=price-ASC&min=0&max=99999&search=&listed=true&fits=all&bid=all'.format(test)
            page = requests.get(URL).json()
            for item in page['items']:
                price = item['price']
                id = item['name'].split('#')[1]
                seller = 'https://solscan.io/account/' + item['seller_address']
                buylink = 'https://solanart.io/search/?token=' + item['token_add']
                img = item['link_img']
                atts = item['attributes'].split(",")
                background = atts[0].split(": ")[1]
                fur = atts[1].split(": ")[1]
                earring = atts[2].split(": ")[1]
                eyes = atts[3].split(": ")[1]
                glasses = atts[4].split(": ")[1]
                hat = atts[5].split(": ")[1]
                mouth = atts[6].split(": ")[1]
                clothing = atts[7].split(": ")[1]
                howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()
        
                row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Solanart", buylink, img, background, fur, earring, eyes, glasses, hat, mouth, clothing]).T
                df = pd.concat([df, row], ignore_index=True)
        
    #Digitaleyes data
    def DE_scrape(URL):
        #URL = 'https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=Meerkat%20Millionaires%20Country%20Club'
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
                earring = atts[2]['value']
                eyes = atts[3]['value']
                glasses = atts[4]['value']
                hat = atts[5]['value']
                mouth = atts[6]['value']
                clothing = atts[7]['value']
                howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()

                row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Digitaleyes", buylink, img, background, fur, earring, eyes, glasses, hat, mouth, clothing]).T
                df = pd.concat([df, row], ignore_index=True)
            if next_curs != None:
                next_URL = DE_url + '&cursor=' + next_curs  
                return DE_scrape(next_URL)
            else:
                pass
        except:
            print("DE Error")

    #Magic Eden data
    def ME_scrape(URL):
        #attys = pd.read_csv('MMCC.csv')
        try:
            global df
            global ranks

            #URL2 = "https://api-mainnet.magiceden.dev/v2/collections/meerkat_millionaires_country_club/listings?offset=0&limit=20?"
            #page = requests.get(URL).json()
            
            stat_url = 'https://api-mainnet.magiceden.dev/v2/collections/meerkat_millionaires_country_club/stats'
            response = requests.get(stat_url).json()
            listed = response['listedCount']

            for vary in range(0,round(listed/20)+2):
                url = 'https://api-mainnet.magiceden.dev/rpc/getListedNFTsByQuery?q=%7B%22$match%22:%7B%22collectionSymbol%22:%22meerkat_millionaires_country_club%22%7D,%22$sort%22:%7B%22takerAmount%22:1,%22createdAt%22:-1%7D,%22$skip%22:{},%22$limit%22:20%7D'.format(vary*20)
                page = requests.get(url).json()

                for item in page['results']:
                    price = item['price']
                    id = item['title'].split('#')[1]
                    seller = 'https://solscan.io/account/' + item['owner']
                    buylink = 'https://www.magiceden.io/item-details/' + item['mintAddress']
                    img = item['img']
                    atts = item['attributes']
                    background = atts[0]['value']
                    fur = atts[1]['value']
                    earring = atts[2]['value']
                    eyes = atts[3]['value']
                    glasses = atts[4]['value']
                    hat = atts[5]['value']
                    mouth = atts[6]['value']
                    clothing = atts[7]['value']
                    howrare_rank = ranks.loc[ranks['ID'] == int(id), 'HowRare.is'].item()
                    moonrank = ranks.loc[ranks['ID'] == int(id), 'MoonRank'].item()

                    row = pd.DataFrame(data = [price, howrare_rank, moonrank, id, seller, "Magic Eden", buylink, img, background, fur, earring, eyes, glasses, hat, mouth, clothing]).T
                    df = pd.concat([df, row], ignore_index=True)
            #print(df)
        except:
            print("ME Error")    


    #run data scrapes
    SA_scrape(SA_url)
    DE_scrape(DE_url)
    ME_scrape(ME_url)

    #format dataframe
    df.columns = ["Price","Rank","MoonRank","ID","Seller Wallet","Market","Listing Link","Image","Background","Fur","Earring","Eyes","Glasses","Hat","Mouth","Clothing"]
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

    #Side bar data
    st.sidebar.title("Attribute Filters")

    rank_type = st.sidebar.selectbox('Ranking Filtering Method:', ['Howrare.is', 'MoonRank'])

    rank_choice = st.sidebar.number_input('Max Meerkat Rank:', min_value = 1, max_value = 9999, step = 1, value = 9999)
    if rank_type == 'Howrare.is':
        df = df[df['Rank'] <= rank_choice]
    else:
        df = df[df['MoonRank'] <= rank_choice]

    market_choice = st.sidebar.selectbox('Market:', ['All', 'Solanart','Digitaleyes','Magic Eden'])
    if market_choice != 'All':
        df = df[df['Market']  == market_choice]

    background_choice = st.sidebar.selectbox('Background:', attributes['Background'])
    if background_choice != 'All':
        df = df[df['Background']  == background_choice.split(" (")[0]]

    fur_choice = st.sidebar.selectbox('Fur:', attributes['Fur'])
    if fur_choice != 'All':
        df = df[df['Fur']  == fur_choice.split(" (")[0]]

    earrings_choice = st.sidebar.selectbox('Earrings:', attributes['Earrings'])
    if earrings_choice != 'All':
        df = df[df['Earrings']  == earrings_choice.split(" (")[0]]

    eyes_choice = st.sidebar.selectbox('Eyes:', attributes['Eyes'])
    if eyes_choice != 'All':
        df = df[df['Eyes']  == eyes_choice.split(" (")[0]]

    glasses_choice = st.sidebar.selectbox('Glasses:', attributes['Glasses'])
    if glasses_choice != 'All':
        df = df[df['Glasses']  == glasses_choice.split(" (")[0]]

    hat_choice = st.sidebar.selectbox('Hat:', attributes['Hat'])
    if hat_choice != 'All':
        df = df[df['Hat']  == hat_choice.split(" (")[0]]

    mouth_choice = st.sidebar.selectbox('Mouth:', attributes['Mouth'])
    if mouth_choice != 'All':
        df = df[df['Mouth']  == mouth_choice.split(" (")[0]]

    clothing_choice = st.sidebar.selectbox('Clothing:', attributes['Clothing'])
    if clothing_choice != 'All':
        df = df[df['Clothing']  == clothing_choice.split(" (")[0]]

    # necklace_choice = st.sidebar.selectbox('Necklace:', attributes['Necklace'])
    # if necklace_choice != 'All':
    #     df = df[df['Necklace']  == necklace_choice.split(" (")[0]]


    #Streamlit commands
    col1, col2 = st.columns(2)
    try:
        col1.subheader("MMCC Rewards Pool & Payouts")
        col1.write("**Royalties Pool:** " + str(reward_floor) + " SOL")

        s1 = pd.Series([reward, reward_hold, reward_mint])
        s11 = pd.Series([estimate_both, estimate_hold, estimate_mint])
        Frame = pd.DataFrame(data = [list(s1),list(s11)], index = ["Current SOL Payout","Estimated SOL Payout"], columns = ["Minter + Holder","Holder","Minter"])
        Frame.style.set_properties(**{'text-align': 'left'})
        col1.table(Frame)
    except:
        Frame = pd.DataFrame(data = ["Solscan API Error"])
        col1.table(Frame)

    col2.subheader("MMCC Market Floor Prices")
    col2.write("**Note:** This may be slighty out of sync with the blockchain")
    s2 = pd.Series([SA_floor, DE_floor, ME_floor])
    Frame2 = pd.DataFrame(data = [list(s2)], index = ["Floor Price"], columns = ["Solanart", "Digitaleyes","Magic Eden"])
    Frame2.style.set_properties(**{'text-align': 'left'})
    col2.table(Frame2)

    st.subheader("Current MMCC Market Listings")
    st.write("Data from Solanart, Digitaleyes, and Magic Eden")

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

    def orderbook_chart():
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
        
        def render_stacked_area_chart2():
            cts = df['Price'].value_counts().sort_index()
            cts_list = cts.tolist()

            unique = df['Price'].value_counts().sort_index().keys()
            unique2 = list(df['Price'].value_counts().sort_index().keys())
            cum = df['Price'].value_counts().sort_index().cumsum()
            cum_list = cum.tolist()
            cumSOL = cts*unique
            cumSOL_list = cumSOL.cumsum().tolist()

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
                    "data": ["For Sale", "Cumulative SOL","Cumulative Kats"],
                    "top": 25
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
                "xAxis": [
                    {
                        "name": "Floor Price",
                        "type": "category",
                        "boundaryGap": False,
                        "data": unique2,
                    }
                ],
                "yAxis": [{"type": "value", "name":"Total # Kats/SOL"}],
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
                        "data": cts_list,
                    },
                    {
                        "name": "Cumulative Kats",
                        "type": "line",
                        "stack": "Total",
                        "areaStyle": {},
                        "data": cum_list,
                    },
                    {
                        "name": "Cumulative SOL",
                        "type": "line",
                        "stack": "Total",
                        "areaStyle": {},
                        "data": cumSOL_list,
                    },
                ],
            }
            st_echarts(options=option, height="500px")
        
        render_stacked_area_chart2()


    def pricevrank_chart():
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
                "xAxis": {"name":"Rank"},
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

    def whale_chart():
        st.subheader("OUTDATED MMCC Whale Tracker as of 12-3-2021 2:00 AM UTC")
        c1, c2 = st.columns(2)
        with c1:
            whale = pd.read_csv('MMCC_whales.csv', index_col=False)
            gb2 = GridOptionsBuilder.from_dataframe(whale)
            gb2.configure_pagination()
            gb2.configure_column("Link", cellRenderer=sol_jscode)
            gb2.configure_column("NFTEyez Link", cellRenderer=link_jscode)
            gridOptions2 = gb2.build()
            grid_return1 = AgGrid(whale,allow_unsafe_jscode=True, theme="streamlit", gridOptions=gridOptions2, fit_columns_on_grid_load=True)

        with c2:
            chart = pd.read_csv('MMCC_chart.csv', index_col=False)
            def render_bar_chart():
                option = {
                    "title": {
                    "left": "center",
                    "text": "Meerkat Distribution per Wallet Size (4604 Holders)"
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
    
    def historic_charts():
        con = psycopg2.connect(
                host = os.getenv("DB_HOST", "ec2-35-153-88-219.compute-1.amazonaws.com"),
                database = os.getenv("DB_NAME", "d8moers639v8ep"),
                user = os.getenv("DB_USER", "rtqdsyhnkwqepo"),
                password = os.getenv("DB_PASSWORD", "9756e62250ffd60cbd98b664fc857623393385145d7fd429c67b9186b94d5afc")
        )
        cur = con.cursor()
        floor_data = pd.DataFrame()
        cur.execute("SELECT to_char(date, 'YYYY-MM-DD HH24:00'), SA, DE, ME, listed, holder FROM floor")
        data = cur.fetchall()
        for entry in data:
            date, SA_f, DE_f,ME_f,listed,holder = entry
            row = pd.DataFrame(data = [date, float(SA_f), float(DE_f),float(ME_f),float(listed),float(holder)]).T
            floor_data = pd.concat([floor_data, row], ignore_index=True)
        floor_data.columns = ["Date","SA","DE","ME","Listed","Holder"]
        floor_data.sort_values(by = ['Date'], inplace=True)
        con.close()

        def render_floor():

            option = {
                "title": {
                    "left": "center",
                    "text": "Historic Floor Prices"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
                },
                "legend": {
                    "data": ["Solanart", "Digitaleyes","Magic Eden"],
                    "top": 25,
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
                "xAxis": [
                    {
                        "name": "Time",
                        "type": "category",
                        "boundaryGap": False,
                        "data": floor_data["Date"].tolist(),
                    }
                ],
                "yAxis": [{"type": "value", "name":"Price"}],
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
                        "name": "Solanart",
                        "type": "line",
                        "data": floor_data["SA"].tolist(),
                    },
                    {
                        "name": "Digitaleyes",
                        "type": "line",
                        "data": floor_data["DE"].tolist(),
                    },
                    {
                        "name": "Magic Eden",
                        "type": "line",
                        "data": floor_data["ME"].tolist(),
                    },
                ],
            }
            st_echarts(options=option, height="500px")

        render_floor()

        def render_listed():

            option = {
                "title": {
                    "left": "center",
                    "text": "# Kats Listed"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
                "xAxis": [
                    {
                        "name": "Time",
                        "type": "category",
                        "boundaryGap": False,
                        "data": floor_data["Date"].tolist(),
                    }
                ],
                "yAxis": [{"type": "value", "name":"# Listed", "min": min(floor_data["Listed"].tolist())-20, "max": max(floor_data["Listed"].tolist())+20}],
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
                        "name": "Listed",
                        "type": "line",
                        "data": floor_data["Listed"].tolist(),
                    },
                ],
            }
            st_echarts(options=option, height="500px")
            
        render_listed()

        def render_holders():

            option = {
                "title": {
                    "left": "center",
                    "text": "# Unique Holders"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
                "xAxis": [
                    {
                        "name": "Time",
                        "type": "category",
                        "boundaryGap": False,
                        "data": floor_data["Date"].tolist(),
                    }
                ],
                "yAxis": [{"type": "value", "name":"# Listed", "min": min(floor_data["Holder"].tolist())-20, "max": max(floor_data["Holder"].tolist())+20}],
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
                        "name": "Listed",
                        "type": "line",
                        "data": floor_data["Holder"].tolist(),
                    },
                ],
            }
            st_echarts(options=option, height="500px")
            
        #render_holders()
    
    orderbook_chart()
    # chart = st.radio("Chart to view:", ("Orderbook", "n", "Historic Charts", "Whale Data"))
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
    # if chart == "Orderbook":
    #     orderbook_chart()
    # elif chart == "Price vs. Rank":
    #     pricevrank_chart()
    # elif chart == "Whale Data":
    #     whale_chart()
    # elif chart == "Historic Charts":
    #     historic_charts()

    st.write("**Note:** This may break at any time, feel free to @JG#4765 in the Meerkat discord for help!")
    st_autorefresh(interval=2 * 60 * 1000, key="dataframerefresh")
    #print(df)

#app()
