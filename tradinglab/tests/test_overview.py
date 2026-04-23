"""Test overview — demonstrates test coverage areas.

Full test suite (540+ tests) covers:

Core:
- test_regime_detection.py (12 tests)
  - BULL/NEUTRAAL/BEAR classification
  - SPY vs EMA130 thresholds
  - VIX integration

- test_conviction.py (16 tests)
  - 3 independent signal verification
  - Conviction 0-3 scoring
  - Sizing per conviction level

- test_instrument_selection.py (10 tests)
  - Conv 1-2 → sector ETF
  - Conv 3 → individual stock
  - Sector ETF mapping
  - TOB rate selection

- test_exit_manager.py (14 tests)
  - Take profit (per instrument type)
  - Trailing stop (3%/6%/8% per type)
  - Break-even activation (+3%)
  - Max hold exit
  - Technical exits (RSI, VWAP)

- test_cost_calculator.py (9 tests)
  - TOB rates (0.35% stocks, 0.12% ETFs)
  - TOB caps (€1,600 / €1,300)
  - IBKR tiered commission
  - FX conversion costs

Trading:
- test_short_prevention.py (12 tests)
  - IBKR position check before SELL
  - SELL_PENDING flag
  - No short creation possible

- test_exchange_hours.py (9 tests)
  - Weekend guard (no trading Sat/Sun)
  - NYSE hours (15:30-22:00 CET)
  - LSE hours (09:00-17:30 CET)

- test_ticker_blacklist.py (5 tests)
  - Auto-blacklist after 2x Error 200
  - 24h expiry
  - Skip blacklisted tickers

Crypto:
- test_kraken_exchange.py (8 tests)
  - Connection, ticker, OHLCV
  - Rate limiting
  - Error handling

- test_crypto_regime.py (7 tests)
  - BTC vs EMA200
  - Fear & Greed Index
  - Regime classification

- test_bounce_strategy.py (8 tests)
  - RSI < 30 filter
  - Bollinger Band check
  - Volume filter
  - F&G per-regime filter

- test_dynamic_sizing.py (6 tests)
  - Regime × F&G matrix
  - Max positions per regime
  - Sizing per F&G range

Dashboard:
- test_dashboard_api.py (15 tests)
  - All 14 tabs render
  - Regime endpoint
  - Portfolio endpoint
  - Vergelijking tab

Total: 540+ tests, pytest, ~5s runtime
"""


def test_placeholder():
    """This public repo contains test structure only.
    Full test suite is in the private repository."""
    assert True
