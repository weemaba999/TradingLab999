# TradingLab Architecture

## Decision Flow

```
Market Data (yfinance, IBKR, Kraken)
│
▼
┌─────────────────┐
│ Regime Detection │ ── SPY vs EMA130 (equities)
│                  │    BTC vs EMA200 + F&G (crypto)
└────────┬────────┘
│
▼
┌─────────────────┐
│  Pre-Filters    │ ── VIX > 25: stop
│                 │    Correlation > 0.85: skip
│                 │    Win Rate < 45%: skip
│                 │    Quality Floor < 0.20: skip
└────────┬────────┘
│
▼
┌─────────────────┐
│   Conviction    │ ── 3 independent signals vote
│   Engine        │    0: no trade
│                 │    1: small (ETF)
│                 │    2: medium (ETF)
│                 │    3: large (stock)
└────────┬────────┘
│
▼
┌─────────────────┐
│  Instrument     │ ── Conv 1-2 → Sector ETF (0.12% TOB)
│  Selection      │    Conv 3 → Individual (0.35% TOB)
└────────┬────────┘
│
▼
┌─────────────────┐
│  Order          │ ── IBKR API (equities)
│  Execution      │    Kraken API (crypto)
└────────┬────────┘
│
▼
┌─────────────────┐
│  Exit Manager   │ ── TP: 15% (all instruments)
│                 │    TS: 3% ETF / 6% stock / 8% leveraged
│                 │    Break-even: after +3%
│                 │    Max hold: varies by type
└─────────────────┘
```

## Cost Structure (Belgian Investor)

The entire system is designed around minimizing the impact of
Belgian transaction tax (TOB), which is the dominant cost factor.

See `CostCalculator` in `core/base.py` for the implementation.

## Infrastructure

Two-node Proxmox cluster with dedicated LXC containers per service.
See `infra/` for Docker and deployment configurations.
