company_ticker = ["FB", "TSLA", "GOOGL", "AAPL", "UBER", "LYFT", "AMZN", "MSFT", "NVDA", "NFLX"]

pos_titles = []
neg_titles = []

import requests, os

#positive
for ct in company_ticker:
    path = "data/text/" + ct
    try:
        os.mkdir(path)
    except OSError:
        print("bruh")
        #do nothing


    url = ('https://stocknewsapi.com/api/v1?tickers=' + ct + '&sentiment=positive&sortby=unique&type=article&items=50&token=00wj4gln2dbrxhwuttqilzoirhemfcyn0t0npcdi')
    response = requests.get(url)

    json_file = response.json()

    #saves a copy of raw json file for reference
    f = open("data/text/" + ct + "/pos_data6.txt", "w")
    f.write(str(json_file))


    for a in json_file['data']:
        pos_titles.append(a['title'])


outF = open("data/positive.txt", "a")
for title in pos_titles:
    title = title.replace('\n', '')
    outF.write(title)
    outF.write("\n")
outF.close()

#negative
for ct in company_ticker:
    url = ('https://stocknewsapi.com/api/v1?tickers=' + ct + '&sentiment=negative&sortby=unique&type=article&items=50&token=00wj4gln2dbrxhwuttqilzoirhemfcyn0t0npcdi')
    response = requests.get(url)

    json_file = response.json()

    #saves a copy of raw json file for reference
    f = open("data/text/" + ct + "/neg_data6.txt", "w")
    f.write(str(json_file))


    for a in json_file['data']:
        neg_titles.append(a['title'])


outF = open("data/negative.txt", "a")
for title in neg_titles:
    title = title.replace('\n', '')
    outF.write(title)
    outF.write("\n")
outF.close()