import json
import os
from datetime import datetime
from typing import Dict, Any

import yfinance as yf
from .config import StockConfig


class StockDataDownloader:
    def __init__(self, config: StockConfig):
        self.config = config
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        os.makedirs(self.config.output_dir, exist_ok=True)

    def _format_filename(self, ticker: str) -> str:
        """Generate filename for the stock data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(
            self.config.output_dir,
            f"{ticker}_{self.config.interval.value}_{timestamp}.json"
        )

    def _download_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Download stock data for a given ticker."""
        stock = yf.Ticker(ticker)
        data = stock.history(
            interval=self.config.interval.value,
            period=self.config.period
        )

        # Convert DataFrame to list of records with start and end times
        records = []
        for i in range(len(data)):
            record = data.iloc[i].to_dict()
            record['start_time'] = data.index[i].isoformat()
            # For the end time, use the next record's start time, or current time if it's the last record
            if i < len(data) - 1:
                record['end_time'] = data.index[i + 1].isoformat()
            else:
                record['end_time'] = datetime.now().isoformat()
            records.append(record)

        # Convert DataFrame to dictionary
        data_dict = {
            "ticker": ticker,
            "interval": self.config.interval.value,
            "period": self.config.period,
            "data": records
        }
        return data_dict

    def _save_data(self, data: Dict[str, Any], filename: str) -> None:
        """Save stock data to JSON file."""
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def download_all(self) -> None:
        """Download and save data for all configured tickers."""
        for ticker in self.config.tickers:
            try:
                print(f"Downloading data for {ticker}...")
                data = self._download_stock_data(ticker)
                filename = self._format_filename(ticker)
                self._save_data(data, filename)
                print(f"Data saved to {filename}")
            except Exception as e:
                print(f"Error downloading {ticker}: {str(e)}")
