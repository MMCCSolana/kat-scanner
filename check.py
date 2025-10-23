import requests
import pandas as pd
import streamlit as st
import datetime
import check_data

def app():
    
    #manual entry for holder/minter wallets and values
    hold_wallets = check_data.hold_wallets

    mint_wallets = check_data.mint_wallets

    makeup_wallets = check_data.makeup_wallets                   

    hold_values = check_data.hold_values

    mint_values = check_data.mint_values    

    SOL_values = check_data.SOL_values


    #------------rest is automatic-----------------
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    page = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_last_updated_at=true', headers=headers).json()
    solPrice = page['solana']['usd']

    #generate week # and dates since first payout
    week = int(abs(datetime.date.today() - datetime.date(2021,9,27)).days/7)
    dates = pd.date_range(start='10/4/2021', periods = week,freq='W-MON')

    #convert to blocktime
    BT_dates = [datetime.datetime.timestamp(date) for date in dates]
    day = 6
    BT5_dates = [BTd + 86400*day for BTd in BT_dates] #86400s for 1 day

    #initialize variables for recieved rewards storage
    hold_init = [0] * (week+1)
    mint_init = [0] * (week+1)

    #initialize week # column for dataframe
    wk_gen = ['Week {}'.format(i) for i in range(1, week+2)]
    wk_gen[-1] = 'Makeup'

    #dataframe intialize and UI commands to get wallet input from user
    df = pd.DataFrame(index=[wk_gen], columns=['Holder','Minter','# Held','# Minted'])
    
    st.title('Weekly Rewards Checker (5/19/2022)') 
    st.info("🔍 Enter your Solana wallet address(es) below to check your MMCC weekly rewards history.")
   
    input = st.text_area("Enter your SOL wallets, enter each wallet in a new row", placeholder="Example: EbXvaxV15vjJFV2jD1iuzYAULY4g1Rak2FNX4oJJxa1Y")
    if input =="ni":
        input = "EbXvaxV15vjJFV2jD1iuzYAULY4g1Rak2FNX4oJJxa1Y"

    if input is not None and input.strip():
        wallets = [w.strip() for w in input.splitlines() if w.strip()]
    else:
        wallets = []
    
    if not wallets:
        st.warning("👆 Please enter at least one wallet address above to check rewards.")
        return
    
    # ----------main loop once wallet is entered-------- 
    for wallet in wallets:
        try:
            api_url = f"https://api.solscan.io/account/soltransfer/txs?address={wallet}&offset=0&limit=100000"
            response = requests.get(api_url, headers=headers, timeout=10)
            
            # Check if request was successful
            if response.status_code != 200:
                st.error(f"⚠️ Solscan API returned error {response.status_code}. Please try again in a few moments.")
                st.info("💡 Tip: The Solscan API may be rate limiting requests. Wait 30 seconds and try again.")
                continue
            
            resp = response.json()
            
            # Check if response has expected structure
            if 'data' not in resp or resp['data'] is None:
                st.error("⚠️ No transaction data found for this wallet or API temporarily unavailable.")
                st.info("This could mean: 1) The wallet has no MMCC reward transactions, or 2) Solscan API is having issues.")
                continue
                
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timed out. Solscan API is slow to respond. Please try again.")
            continue
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Network error: {str(e)}")
            continue
        except ValueError:
            st.error("⚠️ Solscan API returned invalid data. The API might be temporarily down or rate limiting your requests.")
            st.info("💡 Solutions:\n- Wait 30-60 seconds and try again\n- Check if your wallet address is correct\n- Try again during off-peak hours")
            continue

        for tx in resp['data']['tx']['transactions']:
            lamports = tx['lamport']/1000000000
            time = tx['blockTime']

            #check for txs that are week 30+
            if tx['src'] in hold_wallets and tx['src'] in mint_wallets:
                idx = [i for i, n in enumerate(BT_dates) if time >= n and time <= BT5_dates[i]][0]
                if round(lamports/hold_values[idx],2) % 1 == 0:
                    hold_init[idx] = hold_init[idx] + lamports
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2) 
                else:
                    mint_init[idx] = mint_init[idx]+ lamports
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)

            #check for holder txs before week 30
            elif tx['src'] in hold_wallets and tx['src'] not in mint_wallets:
                idx = [i for i, n in enumerate(BT_dates) if time >= n and time <= BT5_dates[i]][0]
                if tx['src'] == hold_wallets[idx]:
                    hold_init[idx] = hold_init[idx] + lamports
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2)
                else:
                    hold_init[idx] = hold_init[idx]+ lamports
                    df.loc['Makeup', 'Holder'] = hold_init[idx]

            #check for minter txs before week 30    
            elif tx['src'] in mint_wallets and tx['src'] not in hold_wallets:
                idx = [i for i, n in enumerate(BT_dates) if time >= n and time <= BT5_dates[i]][0]
                if tx['src'] == mint_wallets[idx]:
                    mint_init[idx] = mint_init[idx]+ lamports
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)
                else:
                    mint_init[idx] = mint_init[idx]+ lamports
                    df.loc['Makeup', 'Minter'] = mint_init[idx]
            
            #check for makeup rewards sent out
            elif tx['src'] in makeup_wallets:
                idx = makeup_wallets.index(tx['src'])
                hold_init[idx] = hold_init[idx]+ lamports
                df.loc['Makeup', 'Holder'] = hold_init[idx]

    #dataframe to sum all rewards & show USD value
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

    #Streamlit UI stuff
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
    
#app()
