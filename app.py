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

# Fetch stock data from free API (example using Yahoo Finance)
def get_stock_data():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,TSLA,AMZN"
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
    for stock in stock_data["quoteResponse"]["result"]:
        stock_info = {
            "symbol": stock["symbol"],
            "name": stock["shortName"],
            "price": stock["regularMarketPrice"],
            "volume": stock["regularMarketVolume"],
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
=======
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

# Fetch stock data from free API (example using Yahoo Finance)
def get_stock_data():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,TSLA,AMZN"
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
    for stock in stock_data["quoteResponse"]["result"]:
        stock_info = {
            "symbol": stock["symbol"],
            "name": stock["shortName"],
            "price": stock["regularMarketPrice"],
            "volume": stock["regularMarketVolume"],
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
