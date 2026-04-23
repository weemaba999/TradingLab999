-- TradingLab Database Schema
-- TimescaleDB (PostgreSQL + hypertables)

-- Equities trades
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    prijs DOUBLE PRECISION,
    aantal INTEGER,
    pnl_pct DOUBLE PRECISION,
    pnl_eur DOUBLE PRECISION,
    conviction INTEGER,
    instrument_type VARCHAR(20),
    tob DOUBLE PRECISION,
    commissie DOUBLE PRECISION,
    slippage_pct DOUBLE PRECISION,
    reden TEXT,
    regime VARCHAR(20),
    portfolio VARCHAR(20)
);
SELECT create_hypertable('trades', 'timestamp', if_not_exists => TRUE);

-- Crypto schema
CREATE SCHEMA IF NOT EXISTS crypto;

CREATE TABLE IF NOT EXISTS crypto.ohlcv (
    timestamp TIMESTAMPTZ NOT NULL,
    pair VARCHAR(20) NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    PRIMARY KEY (timestamp, pair)
);
SELECT create_hypertable('crypto.ohlcv', 'timestamp', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS crypto.trades (
    id SERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    pair VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    cost_eur DOUBLE PRECISION,
    fee DOUBLE PRECISION,
    pnl_eur DOUBLE PRECISION,
    pnl_pct DOUBLE PRECISION,
    reden TEXT,
    regime VARCHAR(20),
    portfolio VARCHAR(20),
    conviction INTEGER
);
SELECT create_hypertable('crypto.trades', 'timestamp', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS crypto.open_posities (
    pair VARCHAR(20) PRIMARY KEY,
    entry_prijs DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    kosten_eur DOUBLE PRECISION,
    portfolio VARCHAR(20),
    conviction INTEGER,
    signalen TEXT,
    trailing_stop_pct DOUBLE PRECISION,
    take_profit_pct DOUBLE PRECISION,
    max_hold_dagen INTEGER,
    peak_prijs DOUBLE PRECISION,
    entry_ts TIMESTAMPTZ,
    updated_ts TIMESTAMPTZ DEFAULT NOW(),
    dry_run BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS crypto.regime_snapshot (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    regime VARCHAR(20),
    btc_prijs DOUBLE PRECISION,
    btc_ema200 DOUBLE PRECISION,
    fear_greed INTEGER,
    fear_greed_label VARCHAR(30)
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades (ticker, timestamp);
CREATE INDEX IF NOT EXISTS idx_trades_side ON trades (side, timestamp);
CREATE INDEX IF NOT EXISTS idx_crypto_ohlcv_pair ON crypto.ohlcv (pair, timestamp);
CREATE INDEX IF NOT EXISTS idx_crypto_trades_pair ON crypto.trades (pair, timestamp);
