import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

from io import BytesIO
import base64

RAPIDAPI_KEY = "7b04715a5dmshb9466c2cb98eecep188d44jsn7d8c99c33de6"
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

symbol_string = ""
inputdata = {}

def fetchStockData(symbol):
    response = requests.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=1mo",
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
    #timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    calendertime = []
    for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))
    return calendertime

def parseValues(inputdata):
    valueList = []
    #valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])

    return valueList

def attachEvents(inputdata):

    eventlist = []

    # for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    #     eventlist.append("open")  

    for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")

    return eventlist


def graph(symbol):

    symbol_string = symbol
    retdata = fetchStockData(symbol_string)

    if (None != inputdata):
        inputdata["Timestamp"] = parseTimestamp(retdata)

        fake = []
        comparison = datetime.strptime(inputdata["Timestamp"][0], "%m/%d/%Y")
        for x in range(len(inputdata["Timestamp"])):
            cur = datetime.strptime(inputdata["Timestamp"][x], "%m/%d/%Y")
            delta = cur - comparison
            fake.append(delta.days)
        # for x in range(len(inputdata["Timestamp"])//2):
        #     fake.append(x)

        temp = inputdata["Timestamp"]
        inputdata["Timestamp"] = fake

        inputdata["Values"] = parseValues(retdata)
        inputdata["Events"] = attachEvents(retdata)

        df = pd.DataFrame(inputdata)

        
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df)

    sns.set(style="darkgrid")
    #rcParams['figure.figsize'] = 15,30
    rcParams['figure.subplot.bottom'] = 0.2
    #ax = sns.lineplot(x="Timestamp", y="Values", hue="Events", dashes=False, markers=True, data=df, sort=False)
    ax = sns.lmplot(x="Timestamp", y="Values", fit_reg=True, order=3, data=df)

    coef = np.polyfit(df["Timestamp"], df["Values"], 3).tolist()

    ax.fig.set_size_inches(18.5, 10.5)
    #ax.set_title('Symbol: ' + symbol_string)
    ax.fig.suptitle('Symbol: ' + symbol_string)
    plt.xticks(inputdata["Timestamp"], temp)

    # # resize figure box to -> put the legend out of the figure
    # box = ax.ax.get_position() # get position of figure
    # ax.ax.set_position([box.x0, box.y0, box.width * 0.85, box.height]) # resize position

    # # Put a legend to the right side
    # ax.ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)


    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='xx-small'
        )
    plt.yticks(
        fontweight='light',
        fontsize='xx-small'
        )

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()




    return (plot_url, coef, inputdata["Timestamp"][len(inputdata["Timestamp"])-1], inputdata["Values"][len(inputdata["Values"])-1])


