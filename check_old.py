import requests
import pandas as pd
import streamlit as st

def app():
    
    #inputs
    week = 15

    hold_wallets = ['GNc185Keqebtg8aKcGW27FGwq1j4k4vG25evVe61CrHE', 'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW',
                    '4zHL5ioFdLVmbK2eHzrvW9zVehR1jhnJqyQodT8fAuhU','52a6HJHqGWNPsjqMGjyWYSdf2KpjwRZ6Kp8bYSLbPQty',
                    'AqpNPzQFqsXngfH2pwtN8xiDpRtAManMU7t2Ku2bE5Hx','BtzWy68tqCYYZVSK9iqLEu1CSnKKwfG9NE5tpr3sJZ6D',
                    '3g1FF1wTyv4guNSZLX5Hb8FYVspv7d1bPKAuK9fXpijq','H8zN9ByTsougVbga5Pyiav3Tse9DyEruXyoceKrBGzFz',
                    '8ATd1GZaZQCmy2frV7bjg9gEqW8vwu5Lao6ydCRuMksd','ANionh4uLhpDRgUWxwCjQ5qPmrhnHEodZ6ngs1WUMPXc',
                    'Cb9EGRp5E45SVzJJVunaRjDAbXGhi1Ez7SmrdayVvYRT','83sE14avcn654GRjs38HDVL1ui8ysSnC2Spkwo8hTabk',
                    'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW', 'FFbxRPpeqfSi5gnrhh1iGbqdZ7VyVNDYEbPcgfjktTpd',
                    'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW'
                    ]

    mint_wallets = ['BJrgn9rG2Yht724a9xSzW2NGXNuxMvrkPhr93x8bgS3Q', 'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M',
                    '7hdTiiPfXUVQJhzJwXCQiB3BZz3uydCEPbyxYjbgU8AB', '5T34gvjZn9weBe6Uogxi4em4MPKAc87CHe3yvqp2s5gK',
                    'CjpEdDMam97bGWfTVhKy5RS1Ha1Qizg7nKFmz7P7ZmYz', 'CeHp4cmKbbyey5b4CoTWfJmFCa34otE9nQtghfhiyWys',
                    'HyNFUGdT8ikdytmT36hiXKX6bQdiRL6ztbfsQsXKwgbe', '2WLb1me2uF9xM6iHoXvyhj8zt1k8NtRQLkyPvL7nEGE8',
                    '6aZ58KguXD1zR6xwFhG45yWq853jtKe3qvgWWfgoH4X4', 'A4Kk3SH1HxZr8TGJcF3sTBXns32c4jkXqrEkFVr72QZk',
                    'ABsKmyQNygQpeTTj6jw7Ud1jiAjMpkAZU1awN89Z5Zeu', 'HJJU28gUMCckq9VR6TY639amYQ2jb3XcdCaTEkkPegce',
                    'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M','44z22UtScfZcisUVD9TuV7QJESA2v7oKZSDx5AgCJuMh',
                    'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M'
                    ]

    makeup_wallets = ['4zWrm2oMQGHKqAs3j5xenitorSfQHJeV28S737r23AhM']                     

    hold_values = [1.275, 0.404, 0.165, 0.111, 0.03, 0.0295, 0.0235, 0.021, 0.0125, 0.0101, 0.0065, 0.006275, 0.00575, 0.0275, 0.024]

    mint_values = [0.225, 0.07, 0.024, 0.01625, 0.005, 0.00525, 0.004, 0.0035, 0.0021, 0.0015, 0.001, 0.001, 0.001, 0.00475, 0.0042]     

    SOL_values = [157,144,157,213,203,252,238,220,204,195,155,178,174,168,135]


    #rest is automatic
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    page = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_last_updated_at=true', headers=headers).json()
    solPrice = page['solana']['usd']

    dates = pd.date_range(start='10/4/2021', periods = week,freq='W-MON')

    hold_init = [0] * (week+1)
    mint_init = [0] * (week+1)

    wk_gen = ['Week {}'.format(i) for i in range(1, week+2)]
    wk_gen[-1] = 'Makeup'

    df = pd.DataFrame(index=[wk_gen], columns=['Holder','Minter','# Held','# Minted'])
    
    st.title('Weekly Rewards Checker') 
   
    input = st.text_area("Enter your SOL wallets, enter each wallet in a new row")
    input = "EbXvaxV15vjJFV2jD1iuzYAULY4g1Rak2FNX4oJJxa1Y"
    
    if input is not None:
        wallets = input.splitlines()
    
    for wallet in wallets:
        resp = requests.get("https://api.solscan.io/account/soltransfer/txs?address=" + wallet + "&offset=0&limit=100000", headers=headers).json()
        count1 = 2
        count2 = 2
        for tx in resp['data']['tx']['transactions']:
            if tx['src'] in hold_wallets:
                idx = hold_wallets.index(tx['src'])
                print(idx)
                if idx == 1 and count1 == 2: #week 15 temp fix
                    idx = 14
                    hold_init[idx] = hold_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2)
                    count1 = count1 - 1
                elif idx == 1 and count1 == 1: #week 13 temp fix
                    idx = 12
                    hold_init[idx] = hold_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2)
                    count1 = count1 - 1
                else:
                    hold_init[idx] = hold_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2)
            
            elif tx['src'] in mint_wallets:
                idx = mint_wallets.index(tx['src'])
                if idx == 1 and count2 == 2: #week 13 temp fix
                    idx = 14
                    mint_init[idx] = mint_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)
                    count2 = count2 - 1
                elif idx == 1 and count2 == 1: #week 13 temp fix
                    idx = 12
                    mint_init[idx] = mint_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)
                    count2 = count2 - 1
                else:
                    mint_init[idx] = mint_init[idx]+ tx['lamport']/1000000000 
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)
            
            elif tx['src'] in makeup_wallets:
                idx = makeup_wallets.index(tx['src'])
                hold_init[idx] = hold_init[idx]+ tx['lamport']/1000000000 
                df.loc['Makeup', 'Holder'] = hold_init[idx]

    #sum sol df
    temp_df = pd.DataFrame(data = [df['Holder'][0:week+1].tolist(),df['Minter'][0:week+1].tolist()]).T

    wk_gen2 = ['Week {}'.format(i) for i in range(1, week+2)]
    wk_gen2[-1] = 'Makeup'
    temp_df.index = wk_gen2
    temp_df.columns = ['Holder','Minter']

    temp_df['SUM'] = temp_df.fillna(0)['Holder'] + temp_df.fillna(0)['Minter']
    temp_df['USD'] = temp_df['SUM']*solPrice

    df_sum = pd.DataFrame(data = [temp_df['SUM'].sum(), temp_df['USD'].sum()]).T
    df_sum.columns = (['Sol','USD'])
    df_sum.index = (['Total'])

    col1, col2 = st.columns([1,2.75])

    with col1:
        st.write("You have recieved these rewards:")
        st.table(df)
        st.table(df_sum)

    with col2:
        st.write("Rewards data")
    
        df2 = pd.DataFrame(data = [dates, hold_values, mint_values, SOL_values,hold_wallets, mint_wallets]).T
        df2.index=(['Week {}'.format(i) for i in range(1, week+1)])
        df2.columns=(['Date','Holder Reward','Minter Reward','SOL/USD','Holder Wallet','Mint Wallet'])
        df2['Date'] = df2['Date'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))

        st.table(df2)   
    print(df)

app()
