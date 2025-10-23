import requests
import pandas as pd
import streamlit as st
import datetime
import check_data
import os

def app():
    
    #manual entry for holder/minter wallets and values
    hold_wallets = check_data.hold_wallets

    mint_wallets = check_data.mint_wallets

    makeup_wallets = check_data.makeup_wallets                   

    hold_values = check_data.hold_values

    mint_values = check_data.mint_values    

    SOL_values = check_data.SOL_values

    # Get Helius API key from Streamlit secrets or environment
    helius_api_key = None
    try:
        helius_api_key = st.secrets.get("HELIUS_API_KEY")
    except:
        helius_api_key = os.getenv("HELIUS_API_KEY")

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
            # Use Helius API if key is available, otherwise fall back to Solscan
            if helius_api_key:
                # Helius Enhanced Transactions API with pagination for historical data
                st.info(f"🚀 Using Helius API (fetching historical transaction data)...")
                
                all_transactions = []
                before_signature = None
                page_count = 0
                max_pages = 50  # Limit to prevent infinite loops (5000 transactions max)
                
                # Fetch transactions with pagination
                with st.spinner(f"Fetching transaction history... (page {page_count + 1})"):
                    while page_count < max_pages:
                        api_url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions?api-key={helius_api_key}"
                        if before_signature:
                            api_url += f"&before={before_signature}"
                        
                        response = requests.get(api_url, timeout=20)
                        
                        if response.status_code != 200:
                            if page_count == 0:
                                # First page failed
                                st.error(f"⚠️ Helius API returned error {response.status_code}.")
                                try:
                                    error_detail = response.json()
                                    if isinstance(error_detail, dict) and 'error' in error_detail:
                                        st.error(f"API Error: {error_detail.get('error')}")
                                except:
                                    pass
                                break
                            else:
                                # Got some data, stop pagination
                                st.warning(f"⚠️ Stopped at page {page_count} due to API error. Retrieved {len(all_transactions)} transactions.")
                                break
                        
                        page_data = response.json()
                        
                        if not page_data or not isinstance(page_data, list) or len(page_data) == 0:
                            # No more transactions
                            break
                        
                        all_transactions.extend(page_data)
                        page_count += 1
                        
                        # Update progress
                        if page_count % 5 == 0:
                            st.info(f"📥 Retrieved {len(all_transactions)} transactions so far...")
                        
                        # Get signature of last transaction for next page
                        if len(page_data) > 0 and 'signature' in page_data[-1]:
                            before_signature = page_data[-1]['signature']
                        else:
                            # No more pages
                            break
                        
                        # If we got less than 100 transactions, we've reached the end
                        if len(page_data) < 100:
                            break
                
                st.success(f"✅ Retrieved {len(all_transactions)} total transactions from Helius API")
                transactions = all_transactions
                
                if not transactions:
                    st.warning("⚠️ No transactions found for this wallet.")
                    continue
                    
            else:
                api_url = f"https://api.solscan.io/account/soltransfer/txs?address={wallet}&offset=0&limit=100000"
                st.warning("⚠️ No Helius API key found. Using public Solscan API (may be rate limited). Add HELIUS_API_KEY to Streamlit secrets for better performance.")
                response = requests.get(api_url, headers=headers, timeout=15)
                
                # Check if request was successful
                if response.status_code != 200:
                    st.error(f"⚠️ Solscan API returned error {response.status_code}.")
                    st.info("💡 Tip: Add a Helius API key to Streamlit secrets for higher rate limits!")
                    continue
                
                resp = response.json()
                
                # Solscan format: nested structure
                if 'data' not in resp or resp['data'] is None:
                    st.error("⚠️ No transaction data found for this wallet or API temporarily unavailable.")
                    continue
                transactions = resp['data']['tx']['transactions']
                
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timed out. Please try again.")
            continue
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Network error: {str(e)}")
            continue
        except (ValueError, KeyError) as e:
            st.error("⚠️ API returned invalid data. Please try again later.")
            st.info("💡 If this persists, add a Helius API key to Streamlit secrets for better reliability.")
            continue

        for tx in transactions:
            # Parse transaction data based on API format
            try:
                if helius_api_key:
                    # Helius format - need to parse tokenTransfers
                    time = tx.get('timestamp')
                    if not time:
                        continue
                    
                    # Look for SOL transfers in the transaction
                    native_transfers = tx.get('nativeTransfers', [])
                    for transfer in native_transfers:
                        if transfer.get('toUserAccount') == wallet:
                            lamports = transfer.get('amount', 0) / 1000000000
                            src = transfer.get('fromUserAccount', '')
                        else:
                            continue
                            
                else:
                    # Solscan format
                    lamports = tx.get('lamport', 0) / 1000000000
                    time = tx.get('blockTime')
                    src = tx.get('src', '')
                    
                if not time or lamports == 0:
                    continue
                    
            except (KeyError, TypeError, AttributeError):
                continue

            #check for txs that are week 30+
            if src in hold_wallets and src in mint_wallets:
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
            elif src in hold_wallets and src not in mint_wallets:
                idx = [i for i, n in enumerate(BT_dates) if time >= n and time <= BT5_dates[i]][0]
                if src == hold_wallets[idx]:
                    hold_init[idx] = hold_init[idx] + lamports
                    df.loc['Week ' + str(idx+1), 'Holder'] = hold_init[idx]
                    df.loc['Week ' + str(idx+1), '# Held'] = round(hold_init[idx]/hold_values[idx],2)
                else:
                    hold_init[idx] = hold_init[idx]+ lamports
                    df.loc['Makeup', 'Holder'] = hold_init[idx]

            #check for minter txs before week 30    
            elif src in mint_wallets and src not in hold_wallets:
                idx = [i for i, n in enumerate(BT_dates) if time >= n and time <= BT5_dates[i]][0]
                if src == mint_wallets[idx]:
                    mint_init[idx] = mint_init[idx]+ lamports
                    df.loc['Week ' + str(idx+1), 'Minter'] = mint_init[idx]
                    df.loc['Week ' + str(idx+1), '# Minted'] = round(mint_init[idx]/mint_values[idx],2)
                else:
                    mint_init[idx] = mint_init[idx]+ lamports
                    df.loc['Makeup', 'Minter'] = mint_init[idx]
            
            #check for makeup rewards sent out
            elif src in makeup_wallets:
                idx = makeup_wallets.index(src)
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
