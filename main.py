import requests
from twilio.rest import Client
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score

# using the AAPL DATASET
df = pd.read_csv('AnyDesk/stocks/AAPL.csv')
df= df.drop(columns=['Date'])
df.to_csv('output.csv', index=False)

data = pd.read_csv('output.csv',index_col=False)
data.bfill()

# print(data.describe())
# print(data.info())
# sns.pairplot(data)
# sns.distplot(data["High"])

X = data[['Open', 'Low', 'Close', 'Adj Close', 'Volume']]
# print(X)
y = data['High']
last_value_in_high = y.iloc[-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

# Impute missing values
imputer_x = SimpleImputer(strategy='mean')
X_train_imputed = imputer_x.fit_transform(X_train)

# No imputation on testing data (we want to evaluate on unseen data)
X_test_no_imputation = X_test.copy()  # Avoid modifying original data

# Create and fit the regression model
model = LinearRegression()
model.fit(X_train_imputed, y_train)

prediction = model.predict(X_test_no_imputation)

# Print the single prediction
for i in prediction:
    if (i > last_value_in_high) and (i < last_value_in_high+5):
        expected_rising_value = i-last_value_in_high
        if expected_rising_value > 4:
            # adding the news api
            parameters = {
                "q": "aapl",
                "from": "2024-06-05",
                "sortBy": "publishedAt",
                "apiKey": os.environ.get("NEWS_API_KEY"),
                "language": "en"
            }
            news_api_endpoint = "https://newsapi.org/v2/everything"
            response = requests.get(news_api_endpoint, params=parameters)
            response.raise_for_status()
            articles = response.json()["articles"]
            first_three_articles = articles[:3]

            formt_article = [f"Headline: {article['title']}.\nPrediction: Apple stocks expected to go up by {expected_rising_value} \nBrief: {article['description']}" for article in first_three_articles]

            # twilio api to send sms to myself
            account_sid = os.environ.get("TWILIO_ACCOUNT_SSID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
            client = Client(account_sid, auth_token)
            for i in formt_article:
                message_to_be_sent = client.messages.create(
                    from_=os.environ.get("TWILIO_SENDER_ACCOUNT_NUMBER"),
                    body=i,
                    to=os.environ.get("TWILIO_RECEIVER_ACCOUNT_NUMBER")
                )
                print(message_to_be_sent.sid)
                