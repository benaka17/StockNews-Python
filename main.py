import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCKKEY = "H3X0E1G19I5W9CQE"
NEWSKEY = "f71062e78b5f49de83ef0366c4939b70"

ACCOUNTSID = "ACa366a929ed835149e4b47ac9e9b02355"
AUTHTOKEN = "00eb6250fcd69815a658d289c56c3d1a"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stockParams = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCKKEY
}

# Set up the API
stockResponse = requests.get(STOCK_ENDPOINT, params=stockParams)
data = stockResponse.json()["Time Series (Daily)"]
dataList = [value for (key, value) in data.items()]

# Get yesterday's closing price
yesterdayData = dataList[0]
yesterdayClose = yesterdayData["4. close"]
print(yesterdayClose)

# Get the day before yesterday's closing stock price
dayBeforeYesterdayData = dataList[1]
dayBeforeYesterdayClose = dayBeforeYesterdayData["4. close"]
print(dayBeforeYesterdayClose)

# Find the positive difference between the two closing prices
difference = float(yesterdayClose) - float(dayBeforeYesterdayClose)
upDown = None
if difference > 0:
    upDown = "🔺"
else:
    upDown = "🔻"

# Work out the percentage difference in price between the two closing prices
diffPercent = round((difference / float(yesterdayClose)) * 100)
print(diffPercent)

# Get news if the change (aka difference) is greater than x
if abs(diffPercent) > 2:
    newsParams = {
        "apiKey": NEWSKEY,
        "qInTitle": COMPANY_NAME,
    }

newsResponse = requests.get(NEWS_ENDPOINT, params=newsParams)
articles = newsResponse.json()["articles"]

# Use python slicing to get hold of three articles
threeArticles = articles[:3]
print(threeArticles)


# Format articles
formattedArticles = [f"{STOCK_NAME}: {upDown}{difference}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in threeArticles]

# Send the messages via Twilio
client = Client(ACCOUNTSID, AUTHTOKEN)

for article in formattedArticles:
    message = client.messages.create(
        body=article,
        from_= "+19855318277",
        to="+41787706672"
    )



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

