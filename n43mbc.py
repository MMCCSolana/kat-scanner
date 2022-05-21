import requests
import pandas as pd
import datetime
import pandas as pd
import json

link = 'https://moonrank.app/mints/nakedmeerkats?after=0&seen=10031&complete=true'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
page = requests.get(link, headers=headers).json() 
nmbc = []

for i in page['mints']:
    token = i['mint']
    nmbc.append(token)

    test = json.dumps(nmbc)

    with open('json_data.json', 'w') as outfile:
        json.dump(test, outfile)

