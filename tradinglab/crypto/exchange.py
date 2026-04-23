"""Kraken Exchange connector.

Handles REST API communication, rate limiting, and error handling.
No trading logic — just the plumbing to talk to Kraken.
"""

import time
import logging
import krakenex
from typing import Optional

log = logging.getLogger("tradinglab.crypto")


class KrakenError(Exception):
    """Kraken API error."""
    pass


class KrakenExchange:
    """Kraken REST API wrapper with retry logic."""

    def __init__(self, api_key: str, private_key: str):
        self.api = krakenex.API(key=api_key, secret=private_key)
        self._last_call = 0
        self._min_interval = 1.0  # seconds between calls

    def _rate_limit(self):
        """Enforce minimum interval between API calls."""
        elapsed = time.time() - self._last_call
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call = time.time()

    def _public(self, method: str, data: dict = None) -> dict:
        """Public API call (no auth required)."""
        self._rate_limit()
        resp = self.api.query_public(method, data=data or {})
        if resp.get("error"):
            raise KrakenError(f"{method}: {resp['error']}")
        return resp["result"]

    def _private(self, method: str, data: dict = None,
                 retries: int = 3) -> dict:
        """Private API call with retry logic."""
        for attempt in range(1, retries + 1):
            try:
                self._rate_limit()
                resp = self.api.query_private(method, data=data or {})
                if resp.get("error"):
                    raise KrakenError(str(resp["error"]))
                return resp["result"]
            except Exception as e:
                log.warning(f"Kraken {method} attempt {attempt}: {e}")
                if attempt == retries:
                    raise KrakenError(
                        f"{method} failed after {retries} attempts: {e}"
                    ) from e
                time.sleep(2 ** attempt)

    def test_connection(self) -> bool:
        """Test API connectivity."""
        try:
            result = self._public("SystemStatus")
            return result.get("status") == "online"
        except:
            return False

    def get_ticker(self, pair: str) -> dict:
        """Get current ticker data for a pair."""
        result = self._public("Ticker", {"pair": pair})
        data = list(result.values())[0]
        return {
            "bid": float(data["b"][0]),
            "ask": float(data["a"][0]),
            "last": float(data["c"][0]),
            "volume": float(data["v"][1]),  # 24h volume
        }

    def get_ohlcv(self, pair: str, interval: int = 60,
                  since: int = None) -> Optional[list]:
        """Get OHLCV candle data."""
        params = {"pair": pair, "interval": interval}
        if since:
            params["since"] = since

        try:
            result = self._public("OHLC", params)
            pair_key = [k for k in result if k != "last"][0]
            return result[pair_key]
        except:
            return None

    def get_account_balance(self) -> dict:
        """Get account balances."""
        return self._private("Balance")

    def get_open_orders(self) -> dict:
        """Get open orders."""
        return self._private("OpenOrders")

    # Order placement methods intentionally omitted
    # from this public repository.
