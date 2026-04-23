"""TradingLab entry point.

Core trading logic is in the private repository.
This public repo demonstrates architecture and methodology.
"""

import sys
from tradinglab.core.utils import setup_logging

log = setup_logging()


def main():
    log.info("TradingLab v0.4.0")
    log.info("This is the public architecture showcase.")
    log.info("Core trading logic is in the private repository.")
    log.info("See README.md for system overview and backtest results.")
    log.info("See docs/ARCHITECTURE.md for decision flow.")
    log.info("See docs/BACKTESTING.md for methodology.")
    sys.exit(0)


if __name__ == "__main__":
    main()
