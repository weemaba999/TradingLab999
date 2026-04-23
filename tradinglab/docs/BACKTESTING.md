# Backtesting Methodology

## Principles

1. **No lookahead bias** — signals use only data available at decision time
2. **Realistic costs** — TOB, IBKR commission, FX conversion, slippage
3. **Walk-forward validation** — out-of-sample testing, not curve fitting
4. **Multiple regimes** — test across BULL, NEUTRAAL, and BEAR separately
5. **Large sample size** — minimum 300 signals before drawing conclusions

## Lessons Learned

### Sample Size Matters

Our initial analysis on 98 crypto signals suggested a trailing stop of 2%.
When we expanded to 560 signals, the optimal was 6%. The first result was
overfit to a small sample. Always validate with more data.

### Per-Regime Analysis is Essential

A strategy that works "on average" may lose money in specific regimes.
BOUNCE crypto strategy:
- BULL: +130% (143 signals)
- NEUTRAAL: +176% (140 signals)
- BEAR: -51% (277 signals)

Running BOUNCE in BEAR would have destroyed the overall result.

### Costs Change Everything

Our equity strategy generated +35,645 EUR in gross profits over 2 years.
After costs:
- With 0.35% TOB (individual stocks): +6,958 EUR net (80% eaten by costs)
- With 0.12% TOB (sector ETFs): +20,940 EUR net (41% in costs)

Same strategy, same signals, 3x different net result — purely from
instrument selection.
