import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import requests
from matplotlib import rcParams

from io import BytesIO
import base64

RAPIDAPI_KEY = "7b04715a5dmshb9466c2cb98eecep188d44jsn7d8c99c33de6"
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

symbol_string = ""
inputdata = {}

def fetchStockData(symbol):
    response = requests.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=3mo",
    headers={
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
        }
    )
    return response.json()

def parseTimestamp(inputdata):
    timestamplist = []
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    calendertime = []
    for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))
    return calendertime

def parseValues(inputdata):
    valueList = []
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])

    return valueList

def attachEvents(inputdata):

    eventlist = []

    for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")  

    for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")

    return eventlist


def graph(symbol):

    symbol_string = symbol
    retdata = fetchStockData(symbol_string)

    if (None != inputdata):
        inputdata["Timestamp"] = parseTimestamp(retdata)
        inputdata["Values"] = parseValues(retdata)
        inputdata["Events"] = attachEvents(retdata)

        df = pd.DataFrame(inputdata)


    sns.set(style="darkgrid")
    rcParams['figure.figsize'] = 13,5
    rcParams['figure.subplot.bottom'] = 0.2
    ax = sns.lineplot(x="Timestamp", y="Values", hue="Events", dashes=False, markers=True, data=df, sort=False)

    ax.set_title('Symbol: ' + symbol_string)

    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='xx-small'
        )

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


