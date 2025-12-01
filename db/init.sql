CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(16) NOT NULL,
    price NUMERIC,
    volume BIGINT,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    latest_trading_day DATE,
    fetched_at TIMESTAMP DEFAULT now()
);
