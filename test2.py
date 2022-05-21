import requests
import pandas as pd
import datetime
import pandas as pd

wallet = 'FLUNK9i7TNDV6C8n73yoRTJXb9mt2JCqEoBkCVZ7ipDK'
#wallet = 'GJZncUXCPb4fsiLDSch3RKDDbUJYVrskyWE7CZ1jkLs5'
#wallet = '343p4HfFZkJSDbHFD6yg2su4hJjX6jY8sqfiKAgqe3v1'

wallets = ['343p4HfFZkJSDbHFD6yg2su4hJjX6jY8sqfiKAgqe3v1','Ewvy8VV3jAW1hqmAA8WkET3L4w8hV4mFKUrAEBvGVsb3',
            '2bbpJV3GHuSehP1hdpWQZDT51e52sV58m6f7ZZxJvbPD']

hold_wallets = ['GNc185Keqebtg8aKcGW27FGwq1j4k4vG25evVe61CrHE', 'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW',
                '4zHL5ioFdLVmbK2eHzrvW9zVehR1jhnJqyQodT8fAuhU','52a6HJHqGWNPsjqMGjyWYSdf2KpjwRZ6Kp8bYSLbPQty',
                'AqpNPzQFqsXngfH2pwtN8xiDpRtAManMU7t2Ku2bE5Hx','BtzWy68tqCYYZVSK9iqLEu1CSnKKwfG9NE5tpr3sJZ6D',
                '3g1FF1wTyv4guNSZLX5Hb8FYVspv7d1bPKAuK9fXpijq','H8zN9ByTsougVbga5Pyiav3Tse9DyEruXyoceKrBGzFz',
                '8ATd1GZaZQCmy2frV7bjg9gEqW8vwu5Lao6ydCRuMksd','ANionh4uLhpDRgUWxwCjQ5qPmrhnHEodZ6ngs1WUMPXc',
                'Cb9EGRp5E45SVzJJVunaRjDAbXGhi1Ez7SmrdayVvYRT','83sE14avcn654GRjs38HDVL1ui8ysSnC2Spkwo8hTabk',
                'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW', 'FFbxRPpeqfSi5gnrhh1iGbqdZ7VyVNDYEbPcgfjktTpd',
                'G5FbQJTfGWwgLxTk1tUe6NpfjAUcY9UBnjKuA2nGqrdW','H8zN9ByTsougVbga5Pyiav3Tse9DyEruXyoceKrBGzFz',
                '36vNGoX8tknepjZYWdb3apk3K5y7FQUpTfBhARVvUGhX','BhgZJKgVe5QCNEW2akorH6rChBzEJ8WdsCGKVZn55CiX',
                'DB92K8XQmtPdro7kTXBgftDNEzx8po5AWEyjAiZQcpGP','C9AJq8QH1aCKsDY7Ze3wZMv2SxY9JfEuKUySNznHscqY',
                'Bsc4M1AcvLRpnCLLRSTB3jrv6XGhcWfB3u8AVDQp9Eq8','A4XT9YFo4o36FV76dSMkYMAocnc48R5uACLW872ccMRi',
                'HmU4yoswnMYkwKfpFkDyyuVuA5ZifDcGWuqtc6wfKGGF','56qPAAh6CGTbiQy8ghJAwbEoGUaA8GA8PqHuHAUE9agd',
                'AJy4n1stBKMfLxdLQPjTo8GX9uRZbXDv5rKwSmQpRnXJ','2dX1PJjBbhzk5GBKR9uQytT9dxYTsv3XYQ4dbi2auyTf',
                'Gf6nRsnAkqqKWVw9qmbsk1gUVp7s8AHQgJ1uEV1KPaS6'
                ]

mint_wallets = ['BJrgn9rG2Yht724a9xSzW2NGXNuxMvrkPhr93x8bgS3Q', 'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M',
                '7hdTiiPfXUVQJhzJwXCQiB3BZz3uydCEPbyxYjbgU8AB', '5T34gvjZn9weBe6Uogxi4em4MPKAc87CHe3yvqp2s5gK',
                'CjpEdDMam97bGWfTVhKy5RS1Ha1Qizg7nKFmz7P7ZmYz', 'CeHp4cmKbbyey5b4CoTWfJmFCa34otE9nQtghfhiyWys',
                'HyNFUGdT8ikdytmT36hiXKX6bQdiRL6ztbfsQsXKwgbe', '2WLb1me2uF9xM6iHoXvyhj8zt1k8NtRQLkyPvL7nEGE8',
                '6aZ58KguXD1zR6xwFhG45yWq853jtKe3qvgWWfgoH4X4', 'A4Kk3SH1HxZr8TGJcF3sTBXns32c4jkXqrEkFVr72QZk',
                'ABsKmyQNygQpeTTj6jw7Ud1jiAjMpkAZU1awN89Z5Zeu', 'HJJU28gUMCckq9VR6TY639amYQ2jb3XcdCaTEkkPegce',
                'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M','44z22UtScfZcisUVD9TuV7QJESA2v7oKZSDx5AgCJuMh',
                'BL6FcJaaBh8gS6scKM7Bwjpom2Zt1qGdX2YtHPKSuh1M','2WLb1me2uF9xM6iHoXvyhj8zt1k8NtRQLkyPvL7nEGE8',
                '68aBJisxpU173vmj4VnXi4ES4K9MsF95vSHm9PyqwLbM','6JmjV6ZUdJX5p4zhez9gHQBSsaQ4p5HJ1QeGWCANvGff',
                '6QoPVFXqbSx546w6QEmncnSAP9jcX6XDJV7mztrTu9gR','FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX',
                'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX','FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX',
                'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX','FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX',
                'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX','FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX',
                'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX'
                ]

makeup_wallets = ['4zWrm2oMQGHKqAs3j5xenitorSfQHJeV28S737r23AhM']                     

hold_values = [1.275, 0.404, 0.165, 0.111, 0.03, 0.0295, 0.0235, 0.021, 
                0.0125, 0.0101, 0.0065, 0.006275, 0.00575, 0.0275, 0.024, 
                0.0115, 0.0115, 0.0122, 0.010525, 0.00475, 0.00385, 0.00515,
                0.0085, 0.002125, 0.0012, 0.006375, 0.003825]

mint_values = [0.225, 0.07, 0.024, 0.01625, 0.005, 0.00525, 0.004, 0.0035, 
                0.0021, 0.0015, 0.001, 0.001, 0.001, 0.00475, 0.0042, 0.002, 
                0.002, 0.0021, 0.001875, 0.0009, 0.000675, 0.001, 0.0015, 0.000375,
                0.000225,0.00112, 0.000675]         

dates = pd.date_range(start='10/4/2021', periods = 27,freq='W-MON')

link = 'https://api.solscan.io/account/soltransfer/txs?address=' + wallet + '&offset=0&limit=10000000'

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
page = requests.get(link, headers=headers).json()                    

df = pd.DataFrame()
# WALLET CHECKER
# blah = 0
# blah2 = 0
# for i in page['data']['tx']['transactions']:
#     if i['src'] == 'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX':
#         print(str(i['lamport']/1000000000) + '     From:' + i['src'])
#         blah = blah + i['lamport']/1000000000
#     elif i['lamport']/1000000000 >= 1:
#         print(str(i['lamport']/1000000000) + '     ' + i['src'] + ' -> ' + i['dst'] + '   ' + 'https://solscan.io/tx/' + i['txHash'])
#         #print('https://solscan.io/tx/' + i['txHash'])
#         blah2 = blah2 + i['lamport']/1000000000
#         temp = i['dst']
# print(' ')        
# print('int depo from Flar   ' + str(blah))
# print('#Drained  ' + str(blah2) + '   to:  ' + temp)

## CHECK WALLET FOR THESE 5 WALLETS        
# blah = 0
# blah2 = 0
# blah3 = 0
# blah4 = 0
# blah5 = 0
# blah6 = 0
# blah7 = 0
# for i in page['data']['tx']['transactions']:
#     if i['dst'] == 'HU8PBVuTW19fRWmwpjiLSgSUG8WEzrd3Nx8bU8rdtZG5':
#         blah = blah + i['lamport']/1000000000
#     elif i['dst'] == '5EBPWRPbKR3pUGZ1GUUvi12r6NG6ahBTDFg4ub2CMzst':
#         blah2 = blah2 + i['lamport']/1000000000
#     elif i['dst'] == 'AgdoyDmFnWa6nuudfL93DtWRRFrjgLAonvjuwx1cBRv4':
#         blah3 = blah3 + i['lamport']/1000000000
#     elif i['dst'] == 'EYuES5aFtHeyofa1dmx5U2X8mLEHT596yRgA3BuNJwUY':
#         blah4 = blah4 + i['lamport']/1000000000 
#     elif i['dst'] == '343p4HfFZkJSDbHFD6yg2su4hJjX6jY8sqfiKAgqe3v1':
#         blah5 = blah5 + i['lamport']/1000000000 
#     elif i['dst'] == '2bbpJV3GHuSehP1hdpWQZDT51e52sV58m6f7ZZxJvbPD':
#         blah6 = blah6 + i['lamport']/1000000000  
#     elif i['dst'] == 'Ewvy8VV3jAW1hqmAA8WkET3L4w8hV4mFKUrAEBvGVsb3':
#         blah7 = blah7 + i['lamport']/1000000000    

# print(wallet)      
# print(str(blah) + '  HU8PBVuTW19fRWmwpjiLSgSUG8WEzrd3Nx8bU8rdtZG5')
# print(str(blah2) + '  5EBPWRPbKR3pUGZ1GUUvi12r6NG6ahBTDFg4ub2CMzst')       
# print(str(blah3) + '  AgdoyDmFnWa6nuudfL93DtWRRFrjgLAonvjuwx1cBRv4')   
# print(str(blah4) + '  EYuES5aFtHeyofa1dmx5U2X8mLEHT596yRgA3BuNJwUY')  
# print(str(blah5) + '  343p4HfFZkJSDbHFD6yg2su4hJjX6jY8sqfiKAgqe3v1') 
# print(str(blah6) + '  2bbpJV3GHuSehP1hdpWQZDT51e52sV58m6f7ZZxJvbPD') 
# print(str(blah7) + '  Ewvy8VV3jAW1hqmAA8WkET3L4w8hV4mFKUrAEBvGVsb3') 

# FLAR WALLET NON HOLDER/MINTER CHECKER

# blah = 0
# for i in page['data']['tx']['transactions']:
#     if i['lamport']/1000000000 >= 1 and i['dst'] not in hold_wallets and i['dst'] not in mint_wallets:
#         print(str(datetime.datetime.fromtimestamp(i['blockTime'])) + ' || ' + str(int(i['lamport']/1000000000)) + ' SOL || ' + i['src'][0:6] + '...' + i['src'][-4:] + ' -> ' + i['dst'][0:6] + '...' + i['dst'][-4:] + ' || ' + 'https://solscan.io/tx/' + i['txHash'])
#         blah = blah + i['lamport']/1000000000
#         #print('https://solscan.io/tx/' + i['txHash'])
# print('Total SOL: ' + str(blah))

# blah = 0
# for i in page['data']['tx']['transactions']:
#     if i['lamport']/1000000000 >= 1:
#         print(str(datetime.datetime.fromtimestamp(i['blockTime'])) + ' || ' + str(int(i['lamport']/1000000000)) + ' SOL || ' + i['src'][0:6] + '...' + i['src'][-4:] + ' -> ' + i['dst'][0:6] + '...' + i['dst'][-4:] + ' || ' + 'https://solscan.io/tx/' + i['txHash'])
#         blah = blah + i['lamport']/1000000000
#         row = pd.DataFrame(data = [datetime.datetime.fromtimestamp(i['blockTime']), int(i['lamport']/1000000000), i['src'][0:6] + '...' + i['src'][-4:], i['dst'][0:6] + '...' + i['dst'][-4:], 'https://solscan.io/tx/' + i['txHash']]).T
#         df = df.append(row)
#         #print('https://solscan.io/tx/' + i['txHash'])
# print('Total SOL: ' + str(blah))
# df.columns = ['Date','SOL','From:','To:','TX Link']
# df.reset_index(drop=True, inplace=True)
# df.to_csv("presale.csv")  
# print(df)


## WEEKLY WALLET CHECKER

for week in range(25,26):
    df = pd.DataFrame()
    type = 'hold'
    if type == 'mint':
        wallet = mint_wallets[week-1]
        portion = mint_values[week-1]
    else:
        wallet = hold_wallets[week-1]
        portion = hold_values[week-1]

    date = datetime.datetime.timestamp(dates[week-1])
    date2 = date+345600
    date3 = date-172800

    link = 'https://api.solscan.io/account/soltransfer/txs?address=' + wallet + '&offset=0&limit=10000000'

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    page = requests.get(link, headers=headers).json() 

    for i in page['data']['tx']['transactions']:
        #if i['src'] != 'FLARQdNnEz8qzGD5oS67eZbSmY94dqx5RheRXJmHjsaX' and i['dst'] not in wallets:
        #if i['dst'] not in wallets and i['blockTime'] <= date2 and i['blockTime'] >= date3:
        if i['blockTime'] <= date2 and i['blockTime'] >= date3:
            lamps = i['lamport']/1000000000
            ports = lamps / portion
            BTime = i['blockTime']
            date = datetime.datetime.fromtimestamp(BTime)
            row = pd.DataFrame(data = [date, ports , lamps, i['src'][0:6] + '...' + i['src'][-4:],i['dst'][0:6] + '...' + i['dst'][-4:],'https://solscan.io/account/' + i['dst']]).T
            if i['dst'] not in df:
                df = df.append(row)
            else:
                print('repeat: ' + i['dst'])
    df.columns = ['Date', '# Portions','SOL','From:','To:','Link']
    df.sort_values(by = ['# Portions'], inplace=True,ascending=False)
    df.reset_index(drop=True, inplace=True)
    #df.to_csv('Wk' + str(week) + '_' + type + ".csv")  
    df.to_csv("test.csv")
    print(df)
    if mint_wallets.count(wallet) > 1:
        print(week, sum(df['# Portions']), 'CAUTION: MULTIPLE WEEK USE')
    if hold_wallets.count(wallet) > 1:
        print(week, sum(df['# Portions']), 'CAUTION: MULTIPLE WEEK USE')
    else:
        print(week, sum(df['# Portions']))
    #staked kats 524