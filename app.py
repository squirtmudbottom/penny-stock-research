import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests
import sqlite3
from datetime import datetime

app = FastAPI()

# Setup database if it doesn't exist
def setup_db():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        symbol TEXT,
                        name TEXT,
                        price REAL,
                        volume INTEGER,
                        sentiment TEXT,
                        recommendation TEXT)''')
    conn.commit()
    conn.close()

setup_db()

# Analyze stock performance and return sentiment & recommendation
def analyze_stock(price, volume):
    if price > 300:
        sentiment = "Bullish"
        recommendation = "Strong Buy"
    elif price > 200:
        sentiment = "Positive"
        recommendation = "Buy"
    elif price > 100:
        sentiment = "Neutral"
        recommendation = "Hold"
    else:
        sentiment = "Bearish"
        recommendation = "Sell"
    
    # Adjust based on high trading volume
    if volume > 50_000_000:
        recommendation += " - High Volume"

    return sentiment, recommendation

# Fetch stock data from Alpha Vantage
def get_stock_data(symbol):
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not API_KEY:
        return {"error": "Missing API Key"}

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data:
            price = float(data["Global Quote"]["05. price"])
            volume = int(data["Global Quote"]["06. volume"])

            sentiment, recommendation = analyze_stock(price, volume)

            return {
                "symbol": symbol,
                "name": symbol,  
                "price": price,
                "volume": volume,
                "sentiment": sentiment,
                "recommendation": recommendation
            }
    return {"error": f"Failed to fetch data for {symbol}"}

@app.get("/")
def read_root():
    return {"message": "Hello, Penny Stock Research API is running!"}

@app.get("/top-stocks")
def fetch_top_stocks():
    stock_symbols = ["AAPL", "TSLA", "AMZN"]  # Expandable
    results = []
    best_stock = None

    for symbol in stock_symbols:
        stock_info = get_stock_data(symbol)
        if "error" not in stock_info:
            results.append(stock_info)

            # Determine the best stock pick
            if not best_stock or stock_info["recommendation"].startswith("Strong Buy"):
                best_stock = stock_info

            # Store data in the database
            conn = sqlite3.connect("stocks.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO stocks (date, symbol, name, price, volume, sentiment, recommendation) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           (datetime.now().strftime("%Y-%m-%d"), stock_info["symbol"], stock_info["name"], stock_info["price"], stock_info["volume"], stock_info["sentiment"], stock_info["recommendation"]))
            conn.commit()
            conn.close()
    
    return {
        "top_stocks": results,
        "best_pick": best_stock
    }
    from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

