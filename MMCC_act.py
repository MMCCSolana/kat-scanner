import requests
import pandas as pd
import datetime
import streamlit as st
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def app():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    link = 'https://api-mainnet.magiceden.dev/rpc/getGlobalActivitiesByQuery?q=%7B%22%24match%22%3A%7B%22txType%22%3A%7B%22%24in%22%3A%5B%22exchange%22%2C%22acceptBid%22%2C%22auctionSettled%22%5D%7D%2C%22collection_symbol%22%3A%22meerkat_millionaires_country_club%22%7D%2C%22%24sort%22%3A%7B%22blockTime%22%3A-1%2C%22createdAt%22%3A-1%7D%2C%22%24skip%22%3A0%7D'
    page = requests.get(link, headers=headers).json() 

    df = pd.DataFrame()

    counter = 1
    for tx in page['results']:
        try:
            counter = counter + 1
            if tx['source'] == 'magiceden_v2':
                if tx['txName'] == 'buy_now':
                    time = datetime.datetime.fromtimestamp(tx['blockTime'])
                    buyer = tx['buyer_address']
                    buyer_link = 'https://solscan.io/account/' + buyer
                    short_buyer = buyer[0:6] + '...' + buyer[-4:]
                    sig = tx['transaction_id']
                    sig_link = 'https://solscan.io/tx/' + sig
                    token = tx['mint']
                    token_link = 'https://solscan.io/token/' + token
                    short_token = token[0:6] + '...' + token[-4:]
                    seller = tx['seller_address']
                    seller_link = 'https://solscan.io/account/' + seller
                    short_seller = seller[0:6] + '...' + seller[-4:]
                    name = tx['mintObject']['title'].split('#')[1]
                    price = tx['parsedTransaction']['total_amount']/1000000000

                    row = pd.DataFrame(data = [time, name, price, short_buyer, short_seller, short_token, buyer_link, seller_link, token_link, sig_link]).T
                    df = pd.concat([df, row], ignore_index=True)
            else:
                print('TX ',tx['_id'], tx['source'])
        except:
            print('error in TX ',tx['_id'])
    df.columns = ['Time', 'Kat #', 'Price', 'Buyer', 'Seller', 'Token', 'Buyer Link','Seller Link', 'Token Link','TX']
    df.reset_index(drop=True, inplace=True)

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

    gb.configure_column('Buyer Link', cellRenderer=link_jscode)
    gb.configure_column('Seller Link', cellRenderer=link_jscode)
    gb.configure_column('Token Link', cellRenderer=sol_jscode)
    gb.configure_column('TX', cellRenderer=sol_jscode)
    gridOptions = gb.build()
    st.subheader('Recent MMCC Sales')
    st.write('Data from Magic Eden')
    AgGrid(df,allow_unsafe_jscode=True, theme='streamlit', gridOptions=gridOptions, fit_columns_on_grid_load=True)

    st.subheader('Top Sellers, Buyers, & Token Transfers')
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write('**Top Sellers**')
        cts = df['Seller'].value_counts()
        df1 = pd.DataFrame(data = cts)
        df1.reset_index(inplace=True)
        df1 = df1.rename(columns = {'Seller':'Sold'})
        df1 = df1.rename(columns = {'index':'Seller'})
        gb1 = GridOptionsBuilder.from_dataframe(df1)
        gb1.configure_pagination()
        gridOptions1 = gb1.build()
        AgGrid(df1,allow_unsafe_jscode=True, theme='streamlit', gridOptions=gridOptions1, fit_columns_on_grid_load=True)

    with col2:
        st.write('**Top Buyers**')
        cts = df['Buyer'].value_counts()
        df2 = pd.DataFrame(data = cts)
        df2.reset_index(inplace=True)
        df2 = df2.rename(columns = {'Buyer':'Bought'})
        df2 = df2.rename(columns = {'index':'Buyer'})
        gb1 = GridOptionsBuilder.from_dataframe(df2)
        gb1.configure_pagination()
        gridOptions1 = gb1.build()
        AgGrid(df2,allow_unsafe_jscode=True, theme='streamlit', gridOptions=gridOptions1, fit_columns_on_grid_load=True)
    
    with col3:
        st.write('**Top Token Transfers**')
        cts = df['Token'].value_counts()
        df3 = pd.DataFrame(data = cts)
        df3.reset_index(inplace=True)
        df3 = df3.rename(columns = {'Token':'Transfers'})
        df3 = df3.rename(columns = {'index':'Token'})
        gb1 = GridOptionsBuilder.from_dataframe(df3)
        gb1.configure_pagination()
        gridOptions1 = gb1.build()
        AgGrid(df3,allow_unsafe_jscode=True, theme='streamlit', gridOptions=gridOptions1, fit_columns_on_grid_load=True)

#app()