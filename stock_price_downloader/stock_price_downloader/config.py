from pydantic import BaseModel
from typing import List
from enum import Enum


class TimeInterval(str, Enum):
    DAILY = "1d"
    HOURLY = "1h"
    MINUTE = "1m"


class StockConfig(BaseModel):
    tickers: List[str]
    interval: TimeInterval = TimeInterval.DAILY
    period: str = "1y"  # Default to 1 year of data
    output_dir: str = "data"


# Default configuration
DEFAULT_CONFIG = StockConfig(
    tickers=["AAPL", "MSFT", "GOOGL"],
    interval=TimeInterval.DAILY,
    period="1y",
    output_dir="data"
)
