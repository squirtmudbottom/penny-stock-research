from fastapi import FastAPI
import requests
import sqlite3
from datetime import datetime

app = FastAPI()

# Database Setup
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

# Root endpoint to check if API is running
@app.get("/")
def read_root():
    return {"message": "Hello, Penny Stock Research API is running!"}

# Fetch stock data from a free API (example using Alpha Vantage)
def get_stock_data():
    API_KEY = "your_alpha_vantage_key"  # Replace with environment variable in production
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@app.get("/top-stocks")
def fetch_top_stocks():
    stock_data = get_stock_data()
    if not stock_data:
        return {"error": "Failed to fetch stock data"}
    
    results = []
    # Placeholder logic for processing Alpha Vantage response
    for symbol in ["AAPL", "TSLA", "AMZN"]:  # Example stock symbols
        stock_info = {
            "symbol": symbol,
            "name": f"Company {symbol}",
            "price": 150.0,  # Placeholder for real price
            "volume": 1000000,  # Placeholder for real volume
            "sentiment": "Neutral",  # Placeholder
            "recommendation": "Hold"  # Placeholder
        }
        results.append(stock_info)
        
        # Save to DB
        conn = sqlite3.connect("stocks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stocks (date, symbol, name, price, volume, sentiment, recommendation) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (datetime.now().strftime("%Y-%m-%d"), stock_info["symbol"], stock_info["name"], stock_info["price"], stock_info["volume"], stock_info["sentiment"], stock_info["recommendation"]))
        conn.commit()
        conn.close()
    
    return results
