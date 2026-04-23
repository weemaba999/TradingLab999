"""Utility functions — logging, formatting, helpers.
No trading logic here, just infrastructure code."""

import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def setup_logging(name: str = "tradinglab",
                  level: str = "INFO") -> logging.Logger:
    """Configure structured logging."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-5s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def format_pnl(pnl_pct: float, pnl_eur: float = None) -> str:
    """Format P&L for display."""
    sign = "+" if pnl_pct >= 0 else ""
    result = f"{sign}{pnl_pct:.2f}%"
    if pnl_eur is not None:
        result += f" ({sign}€{abs(pnl_eur):.2f})"
    return result


def format_conviction(conviction: int) -> str:
    """Format conviction as star rating."""
    return "⭐" * conviction if conviction > 0 else "⊘"


def is_market_open(ticker: str,
                   now: datetime = None) -> bool:
    """Check if the relevant exchange is open.

    NYSE: Mon-Fri 15:30-22:00 CET
    LSE:  Mon-Fri 09:00-17:30 CET
    Crypto: 24/7
    """
    if now is None:
        now = datetime.now()

    # Weekend check
    if now.weekday() >= 5:
        return False

    # LSE tickers
    lse_tickers = {
        'QQQ3', '3USL', 'SMH', 'IITU', 'IUES', 'IUHC',
        'IUFS', 'IUCD', 'IUCS', 'IUMS', 'IUUS', 'CSPX',
        'CNDX', 'EQQQ'
    }

    if ticker in lse_tickers:
        return 9 <= now.hour < 17 or (now.hour == 17 and now.minute <= 30)

    # NYSE/NASDAQ
    if now.hour < 15 or now.hour >= 22:
        return False
    if now.hour == 15 and now.minute < 30:
        return False

    return True


def corrigeer_gbx(ticker: str, price: float) -> float:
    """Correct GBX (pence) to GBP for LSE-listed securities.

    yfinance returns LSE prices in GBX (pence) not GBP.
    IITU at £36.50 comes back as 3650.0 from yfinance.
    This function detects and corrects that.
    """
    gbp_tickers = {
        'QQQ3', '3USL', 'IITU', 'IUES', 'IUHC', 'IUFS',
        'IUCD', 'IUCS', 'IUMS', 'IUUS', 'CSPX', 'CNDX', 'EQQQ'
    }

    if ticker in gbp_tickers and price > 500:
        return price / 100
    return price


def load_json(path: str, default: dict = None) -> dict:
    """Load JSON file with fallback to default."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default or {}


def save_json(path: str, data: dict):
    """Save dict to JSON file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
