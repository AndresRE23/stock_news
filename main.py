import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_stock_key = os.getenv("API_STOCK_KEY")
api_news_key =  os.getenv("API_NEWS_KEY")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_stock_key
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()

time_series = data["Time Series (Daily)"]
dates = sorted(time_series.keys(), reverse=True)

yesterday = dates[0]
day_before_yesterday = dates[1]

stock_yesterday = float(time_series[yesterday]["4. close"])
stock_day_before = float(time_series[day_before_yesterday]["4. close"])
percentage_change = ((stock_yesterday - stock_day_before) / stock_day_before) * 100

if abs(percentage_change) >= 0:
    parameters = {
        "q": COMPANY_NAME,
        "from": (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat(),
        "sortBy": "publishedAt",
        "pageSize": 3,
        "language": "en",
        "apiKey": api_news_key
    }

    response = requests.get("https://newsapi.org/v2/everything", params=parameters)
    articles = response.json()["articles"]
    print(articles)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
"""

