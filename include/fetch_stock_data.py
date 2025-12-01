import os
import logging
import requests
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger("fetch_stock_data")
if not logger.handlers:
    import sys
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_BASE = "https://www.alphavantage.co/query"
SYMBOL = os.getenv("STOCK_SYMBOL", "GOOGL")

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

def fetch_global_quote(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_KEY
    }
    logger.info("Fetching stock data for %s", symbol)
    resp = requests.get(ALPHA_BASE, params=params)
    data = resp.json()
    return data.get("Global Quote", {})
    
def run_fetch_and_load(**context):
    quote = fetch_global_quote(SYMBOL)
    if not quote:
        logger.error("No data received")
        return False

    parsed = {
        "symbol": quote.get("01. symbol"),
        "price": quote.get("05. price"),
        "volume": quote.get("06. volume"),
        "open_price": quote.get("02. open"),
        "high_price": quote.get("03. high"),
        "low_price": quote.get("04. low"),
        "latest_trading_day": quote.get("07. latest trading day"),
        "fetched_at": datetime.utcnow()
    }

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    sql = """
        INSERT INTO stock_data
        (symbol, price, volume, open_price, high_price, low_price, latest_trading_day, fetched_at)
        VALUES (%(symbol)s, %(price)s, %(volume)s, %(open_price)s, %(high_price)s, %(low_price)s, %(latest_trading_day)s, %(fetched_at)s)
    """

    cur.execute(sql, parsed)
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Stock data inserted successfully")
    return True
