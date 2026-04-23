<p align="center">
  <img src="https://img.shields.io/badge/TradingLab-Algorithmic%20Trading-blueviolet?style=for-the-badge&logo=chartdotjs&logoColor=white" />
</p>

<h1 align="center">🧪 TradingLab</h1>

<p align="center">
  <strong>A regime-aware, conviction-driven algorithmic trading system</strong><br/>
  <em>Built by a solo developer. Powered by data. Validated by 9,000+ backtested signals.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/IBKR-API-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Kraken-API-7B61FF?style=flat-square" />
  <img src="https://img.shields.io/badge/TimescaleDB-Postgres-blue?style=flat-square&logo=timescale&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Proxmox-Self--Hosted-E57000?style=flat-square&logo=proxmox&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-540+-brightgreen?style=flat-square" />
</p>

---

## What is TradingLab?

TradingLab is a fully autonomous algorithmic trading system that trades **equities** (via Interactive Brokers) and **crypto** (via Kraken) from a self-hosted homelab. It doesn't follow hunches. It follows data.

Every parameter — every take-profit level, every trailing stop, every position size — is derived from rigorous backtesting across **9,000+ signals over 2 years of historical data**. Not curve-fitted. Walk-forward validated.

The system runs 24/7 on a Proxmox cluster, monitors markets in real-time, and sends trade alerts via Telegram. A custom-built dashboard provides full visibility into regime, positions, costs, and performance.

> *"The best trade is the trade you don't take."*
> — What 560 crypto signals taught us about patience.

---

## The Numbers
┌─────────────────────────────────────────────────────────────┐
│                    BACKTEST RESULTS                         │
│                  (2 years, 41 tickers)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Equities (8,464 signals)                                   │
│  ├── Strategy: Conviction + ETF Selection    +201.3%        │
│  ├── SPY Buy & Hold (same period)             +18.9%        │
│  └── Outperformance                          +182.4%        │
│                                                             │
│  Crypto (560 signals)                                       │
│  ├── Strategy: BOUNCE v4 (regime-aware)      +233.8%        │
│  ├── BTC Buy & Hold (same period)              +0.6%        │
│  └── Outperformance                          +233.2%        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

*Past performance does not guarantee future results. These are backtested results with realistic fees, slippage, and tax costs included.*

---

## Architecture
                      ┌──────────────────────┐
                      │    Telegram Alerts    │
                      │  🟢 BUY  💰 SELL     │
                      │  🤖 Guardian Tips     │
                      └──────────┬───────────┘
                                 │
┌──────────────┐          ┌──────────▼───────────┐          ┌──────────────┐
│              │          │                      │          │              │
│  Interactive │◄────────►│    TradingLab Core    │◄────────►│    Kraken    │
│   Brokers    │   REST   │                      │   REST   │   Exchange   │
│   Gateway    │          │  ┌────────────────┐  │          │              │
│              │          │  │ Regime Engine  │  │          └──────────────┘
└──────────────┘          │  │ BULL/NEU/BEAR  │  │
│  └───────┬────────┘  │
│          │           │
│  ┌───────▼────────┐  │          ┌──────────────┐
│  │  Conviction    │  │          │              │
│  │  0 → skip      │  │          │  TimescaleDB │
│  │  1 → ETF  3%   │  │◄────────►│  PostgreSQL  │
│  │  2 → ETF  5%   │  │          │              │
│  │  3 → Stock 8%  │  │          └──────────────┘
│  └───────┬────────┘  │
│          │           │          ┌──────────────┐
│  ┌───────▼────────┐  │          │              │
│  │ Exit Manager   │  │          │    Redis     │
│  │ TP/TS/BE/MaxH  │  │◄────────►│    Cache     │
│  └────────────────┘  │          │              │
│                      │          └──────────────┘
└──────────┬───────────┘
│
┌──────────▼───────────┐
│   Dashboard v7.9     │
│  14 tabs, real-time   │
│  regime, P&L, costs   │
└──────────────────────┘

---

## How It Works

### 🎯 Conviction-Driven Entry

TradingLab doesn't use a single score threshold to decide trades. It uses **conviction** — the count of independent confirmations agreeing on the same trade.

Three independent signals vote:
1. **Technical** — EMA alignment + RSI sweet spot + VWAP position
2. **Volume** — Above-average volume confirms institutional interest
3. **Market** — Broad market direction supports the trade

| Conviction | Decision | Instrument | Sizing |
|:---:|---|---|:---:|
| 0 | **No trade** | — | 0% |
| 1 | Trade | Sector ETF | 3% |
| 2 | Trade | Sector ETF | 5% |
| 3 | Trade | Individual stock | 8% |

*Why ETFs for lower conviction?* One word: **tax**. Belgian transaction tax (TOB) is 0.35% on stocks vs 0.12% on ETFs. Over 8,000 trades, that's €14,000 in savings.

### 📊 Regime-Aware Everything

The system classifies market conditions and adapts its entire behavior:
BULL  (SPY > EMA130)  →  Full trading, momentum entries
NEU   (SPY ≈ EMA130)  →  Selective, tighter stops
BEAR  (SPY < EMA130)  →  Cash or minimal exposure

For crypto, regime detection uses BTC vs EMA200 + the Fear & Greed Index. The system discovered that **F&G < 25 is the only zone where mean-reversion works** — everything above that loses money. In BULL regime, F&G is always > 25, so the filter disables itself. The system figured this out from 560 signals, not from theory.

### 🛡️ Exit Engineering

Every position has four exit mechanisms, each backtested across 200+ parameter combinations:

| Exit Type | Sector ETF | Individual Stock | Leveraged ETF |
|---|:---:|:---:|:---:|
| Take Profit | 15% | 15% | 15% |
| Trailing Stop | 3% | 6% | 8% |
| Break-Even | After +3% | After +3% | After +3% |
| Max Hold | 7 days | 14 days | 5 days |

The **break-even mechanism** shifts the trailing stop to entry price after +3% unrealized profit. Once activated, the trade can never lose money. Backtest showed this single feature improves net returns by +66%.

### 💰 Cost Awareness

TradingLab is obsessively cost-aware. It was built in Belgium, where transaction taxes can destroy a strategy:

| Cost Factor | Per Round-Trip | Annual Impact (1000 RT) |
|---|:---:|:---:|
| TOB (stocks) | 0.70% | €7,000 |
| TOB (ETFs) | 0.24% | €2,400 |
| IBKR Commission | ~0.04% | €400 |
| FX Conversion | 0.06% | €600 |

The ETF instrument selection alone saves **€4,600/year** at 1,000 round-trips. Every trade displayed in the dashboard shows its exact cost breakdown.

---

## Crypto Module

The crypto module trades independently on Kraken with its own regime detection and strategy:
┌────────────────────────────────────────────────────────┐
│ CRYPTO STRATEGY: BOUNCE v4                             │
│                                                        │
│ Entry:  RSI < 30 + Lower Bollinger Band + Volume spike │
│ Filter: Fear & Greed < 25 (NEUTRAAL/BEAR regime)       │
│         No filter in BULL regime                       │
│ Exit:   TS 6% / TP 15% / Break-even +3%               │
│                                                        │
│ Backtest: 560 signals, 17 pairs, 2 years               │
│ Result:  +233.8% net (after 0.25% Kraken fees)         │
│ WR:      48.6% (at F&G < 40 filter)                    │
│                                                        │
│ Dynamic sizing:                                        │
│ ┌──────────┬────────┬────────┬────────┐                │
│ │  Regime  │ F&G<15 │ F&G<25 │ F&G<30 │                │
│ │ BULL     │ 2×25%  │ 3×20%  │ 5×15%  │                │
│ │ NEUTRAAL │ 1×20%  │ 2×15%  │ 2×8%   │                │
│ │ BEAR     │ 0      │ 1×8%   │ 0      │                │
│ └──────────┴────────┴────────┴────────┘                │
│                                                        │
│ Universe: SHIB, ALGO, LINK, XRP, ATOM, AAVE,           │
│           DOGE, SOL, BTC, ETH                           │
│ (Ranked by 2-year per-pair backtest performance)       │
└────────────────────────────────────────────────────────┘

What the backtest revealed:
- **BOUNCE is the only profitable strategy in BEAR markets** (+€306 net vs BTC B&H -€3,002)
- **Trend following lost -1,366% over 2 years** — not implemented
- **Grid trading is fee-negative** at Kraken's 0.25% maker rate — not implemented
- **11 trades per year with 82% win rate** beats 143 trades with 50% win rate
- **TS 6% beats TS 2%** — the initial 98-signal backtest suggested 2%, but 560 signals corrected it. More data fixes overfit.

---

## Dashboard

A custom-built 14-tab dashboard provides full operational visibility:

| Tab | What it shows |
|---|---|
| 🏠 Dashboard | Saldo, dag P&L, open posities, win rate |
| 📈 Signalen | Real-time scanner output, regime, VIX, F&G Index |
| 💼 Posities | Open positions with TP/TS/SL levels, per-instrument type |
| 📊 Performance | Equity curve, per-ticker breakdown, slippage analysis |
| ⚡ Volatility | VIX tracking, turbulence z-score |
| 🤖 AI Insights | GPT-4o trade analysis (experimental) |
| ⚙️ Parameters | Live parameter tuning with Optuna history |
| 🔮 Shadow | Shadow configs running in parallel |
| 🧪 Backtest | Walk-forward validation results |
| 🧠 AI Brain | Guardian agent suggestions and learning |
| 🛡️ Roadmap | Safety gates for live transition |
| 📋 Logs | Decision audit trail, every trade explained |
| 📊 Vergelijking | Side-by-side: equities vs crypto, including all costs |
| ₿ Crypto | Crypto positions, regime, Fear & Greed, dry-run status |

---

## Infrastructure

Self-hosted on a two-node Proxmox cluster:
┌─ pve1 (192.168.1.20) ──────────────────────────────┐
│                                                      │
│  LXC 101: Trading Stack (bot + dashboard + Redis)    │
│  LXC 102: IB Gateway (paper trading, port 4002)      │
│  VM  100: Home Assistant                             │
│  VM  108: Paperless-NGX                              │
│                                                      │
├─ pve2 (192.168.1.210) ─────────────────────────────┐
│                                                      │
│  GPU Server: Ollama (local LLM inference)            │
│  TimescaleDB: PostgreSQL + time-series               │
│                                                      │
├─ Synology NAS ──────────────────────────────────────┤
│  Backups, NFS storage                                │
│                                                      │
├─ DevOps ────────────────────────────────────────────┤
│  Claude Code, development, crypto bot dry-run        │
│                                                      │
└─ UniFi Network ─────────────────────────────────────┘
UDM Pro, managed switches, WiFi 6

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Broker (Equities) | Interactive Brokers TWS API (ib_insync) |
| Broker (Crypto) | Kraken REST API (krakenex) |
| Database | TimescaleDB (PostgreSQL + hypertables) |
| Cache | Redis |
| Optimization | Optuna (walk-forward, nightly) |
| Data | yfinance, Finnhub, Alternative.me (F&G) |
| Containers | Docker + LXC on Proxmox VE |
| Monitoring | Telegram Bot API (Guardian agent) |
| Dashboard | Flask + vanilla JS (no framework bloat) |
| Development | Claude Code (AI-assisted development) |
| CI/Testing | pytest (540+ tests) |

---

## What I Learned Building This

This system was built over ~3 months by a single developer, with AI assistance (Claude Code). Some hard-won lessons:

1. **Your first backtest is always wrong.** Our initial 98-signal analysis said trailing stop 2% was optimal. With 560 signals, it was 6%. More data corrects overfit. Always.

2. **Costs are the strategy.** In Belgium, transaction tax (TOB) at 0.35% on stocks means you need >0.87% per round-trip just to break even. Switching to ETFs (0.12% TOB) turned a losing strategy into a winning one.

3. **The best trade is the one you don't take.** Our crypto bot makes ~11 trades per year. That's it. 82% win rate. The temptation to trade more is the enemy of returns.

4. **Bugs in production are expensive.** A duplicate SELL bug created short positions in leveraged ETFs. On paper trading, it was annoying. On a live account, it would have been catastrophic. Build the circuit breaker before you go live.

5. **Markets don't care about your code.** 540 tests, 14 dashboard tabs, 6 exit mechanisms — none of it matters if the market moves against you. Risk management isn't a feature, it's the product.

---

## Status

| Component | Status | Notes |
|---|:---:|---|
| Equities Bot | 🟢 Running | Paper trading (IBKR) |
| Crypto Bot | 🟢 Running | Dry-run (Kraken) |
| Dashboard | 🟢 Live | 14 tabs, auto-refresh |
| Guardian Agent | 🟢 Active | Telegram alerts, debounced |
| Live Trading | 🟡 Planned | Safety systems being validated |
| Open Source | 🔴 Private | Core strategies are proprietary |

---

## Roadmap to Live
Phase 1: Safety Systems (circuit breaker, kill switch, VIX stop)
Phase 2: Infrastructure (staging vs live separation, DB split)
Phase 3: Shadow Mode (live account, suggestions only)
Phase 4: Soft Launch (50% sizing, 30 days monitoring)
Phase 5: Full Live (if Phase 4 passes all gates)

24 steps. ~50 hours of work. No shortcuts on safety.

---

## Can I Use This?

The core trading strategies and proprietary code are **not open source**. This repository serves as a portfolio piece and technical showcase.

If you're interested in:
- 🤝 Collaboration on algorithmic trading research
- 💬 Discussion about the architecture or approach
- 📊 The backtesting methodology

Feel free to reach out.

---

<p align="center">
  <strong>Built with obsessive attention to cost, risk, and data.</strong><br/>
  <em>Because in trading, the margin between profit and loss is measured in basis points.</em>
</p>

<p align="center">
  <sub>TradingLab is a personal project for educational and research purposes. Nothing in this repository constitutes financial advice. Trading involves risk of loss.</sub>
</p>
