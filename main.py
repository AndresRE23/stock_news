import datetime
import os
from dotenv import load_dotenv
import requests
import smtplib

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
percentage_change = round(((stock_yesterday - stock_day_before) / stock_day_before) * 100)

up_down = None
if percentage_change > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

if abs(percentage_change) >= 5:
    my_email = "andresre2311@gmail.com"
    password = "lztaajelqrvhdkmj"

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

    formatted_articles = [(f"Subject:{COMPANY_NAME}: {up_down} {percentage_change}%\n\nHeadline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in articles]

    with smtplib.SMTP("smtp.gmail.com", 587) as cn:
        cn.starttls()
        cn.login(my_email, password)
        for article in formatted_articles:
            cn.sendmail(my_email, my_email, msg=article.encode("utf-8"))

