import requests
import pandas as pd
import datetime
import streamlit as st

def app():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    SA_link = 'https://api.solanart.io/get_floor_price?collection=meerkatmillionairescc'
    ME_link = 'https://api-mainnet.magiceden.dev/v2/collections/meerkat_millionaires_country_club/stats'

    SA_page = requests.get(SA_link, headers=headers).json() 
    SA_list = SA_page['count_listed']

    ME_page = requests.get(ME_link, headers=headers).json() 
    ME_list = ME_page['listedCount']

    listed = SA_list + ME_list

    wallets = ['FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX', #MMCC royalty [0]
                '4G6GUbn83ToYypFweZ8Yue54ZxansRxtVZgfdqauxafN', #MMCC royalty vault
                '5jhFQvxA79oRRc5ZznYitZkH6CCPxri2nCEv7VS2oaSZ', #NMBC royalty
                'A485b6YYGDWQ4i5v9qWe3dEGAZqx6QqKstNHBNyaftPF', #NMBC royalty vault
                'Vai6f8wn7vob27VczML8ZVYKSAxF5hPYjNixumbnRsv', #MMCC unpaid royalty  Money Magnet
                '4cay3d4CgMTATC3Khwj7tyZHqKy4Eoy59s4FvQhtqGjs', #Main DAO wallet
                'Fr6FGZbZ98uxg3NK1jp2NwrCRbRrmfWkABUxBj1twp1N', #RB funds
                'A4xCfBCr5aJKrsPb5c5ea5cMq4AXobcHgnLMGqFtgchq', #DCF funds
                'mmccxRQPmAt7yfK3fpEnW7mDtQYBMP7zgWaxohEzGm6', #MMCC royalty vault 2 [8]
                ]

    vals = []
    for wallet in wallets:
        link = 'https://api.solscan.io/account?address=' + wallet
        reward_json = requests.get(link,headers=headers).json()
        vals.append(reward_json['data']['lamports']/1000000000)
    #print(vals)

    MMCC_sum = vals[0]+ vals[8]
    MMCC_total = vals[0]+ vals[1] + vals[8]
    holder = MMCC_sum*0.85/(9999-listed)
    #minter = MMCC_sum*0.15/10000
    NMBC_sum = vals[2]+ vals[3]
    DAO_sum = sum(vals[1:8])

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Royalty Balances")
        st.write('MMCC Royalties Balance: ' + str(vals[0]) + ' SOL')
        st.write('MMCC Rewards Wallet Balance: ' + str(vals[8]) + ' SOL')
        st.write('MMCC Vault Balance: ' + str(vals[1]) + ' SOL')
        st.write('**MMCC Rewards Total:** ' + str(MMCC_sum) + ' SOL')
        st.write('**MMCC Total:** ' + str(MMCC_total) + ' SOL')
        st.write('')
        st.write('Current Listed Supply: ' + str(listed))
        st.write('MMCC 85% to Holders: ' + str(MMCC_sum*0.85) + ' SOL [ ' + str(holder) +' SOL/Kat ]')
        st.write('MMCC 15% to DAO: ' + str(MMCC_sum*0.15) + ' SOL')
        st.write('')
        st.write('NMBC Royalties Balance: ' + str(vals[2]) + ' SOL')
        st.write('NMBC Vault Balance: ' + str(vals[3]) + ' SOL')
        st.write('**NMBC Total:** ' + str(NMBC_sum) + ' SOL')
    
    with col2:
        st.subheader("ClubDAO Treasury Assets")
        st.write('Main DAO Vault Balance: ' + str(vals[5]) + ' SOL')
        st.write('Money Magnet Balance: ' + str(vals[4]) + ' SOL')
        st.write('RB Vault Balance: ' + str(vals[6]) + ' SOL')
        st.write('DCF Vault Balance: ' + str(vals[7]) + ' SOL')
        st.write('MMCC Vault Balance: ' + str(vals[1]) + ' SOL')
        st.write('NMBC Vault Balance: ' + str(NMBC_sum) + ' SOL')
        st.write('')
        st.write('**Total DAO Treasury:** ' + str(DAO_sum) + ' SOL')
        st.write('**Total DAO Treasury (w/ Minter shares):** ' + str(DAO_sum + MMCC_sum*0.15) + ' SOL')
        st.write('')
        st.subheader("Wallet Links")
        st.write("[Main DAO Wallet](https://solscan.io/account/4cay3d4CgMTATC3Khwj7tyZHqKy4Eoy59s4FvQhtqGjs)")
        st.write("[DAO NFT Wallet](https://solscan.io/account/Dn1G2mh9VdZg9VoX62i545domg25Jbvx7VwuiXNyV6Qe)")
        st.write("[Money Magnet Wallet](https://solscan.io/account/Vai6f8wn7vob27VczML8ZVYKSAxF5hPYjNixumbnRsv)")
        st.write("[RB Funds Wallet](https://solscan.io/account/Fr6FGZbZ98uxg3NK1jp2NwrCRbRrmfWkABUxBj1twp1N)")
        st.write("[DCF Funds Wallet](https://solscan.io/account/A4xCfBCr5aJKrsPb5c5ea5cMq4AXobcHgnLMGqFtgchq)")
        st.write("[MMCC Royalty Wallet](https://solscan.io/account/FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX)")
        st.write("[MMCC Royalty Vault](https://solscan.io/account/4G6GUbn83ToYypFweZ8Yue54ZxansRxtVZgfdqauxafN)")
        st.write("[MMCC Royalty Distribution](https://solscan.io/account/mmccxRQPmAt7yfK3fpEnW7mDtQYBMP7zgWaxohEzGm6)")
        st.write("[NMBC Royalty Wallet](https://solscan.io/account/5jhFQvxA79oRRc5ZznYitZkH6CCPxri2nCEv7VS2oaSZ)")
        st.write("[NMBC Royalty Vault](https://solscan.io/account/A485b6YYGDWQ4i5v9qWe3dEGAZqx6QqKstNHBNyaftPF)")

#app()