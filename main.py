import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCKKEY = "YOUR_STOCK_KEY"
NEWSKEY = "YOUR_NEWS_KEY"

ACCOUNTSID = "YOUR_ACCOUNT_ID"
AUTHTOKEN = "YOUR_AUTHORISATION_TOKEN"

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
        from_= "+YOUR_TWILIO_NUMBER",
        to="+YOUR_PHONE_NUMBER"
    )




