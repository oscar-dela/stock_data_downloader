# Stock Price Downloader

A Python package for downloading historical stock prices and saving them in JSON format.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stock_price_downloader.git
cd stock_price_downloader

# Install dependencies using Poetry
poetry install
```

## Usage

The package can be used both as a command-line tool and as a Python library.

### Command Line Usage

```bash
# Download daily data for multiple stocks
poetry run python -m stock_price_downloader.cli --tickers AAPL MSFT GOOGL --interval 1d --period 1y

# Download hourly data
poetry run python -m stock_price_downloader.cli --tickers AAPL --interval 1h --period 1mo

# Download minute data
poetry run python -m stock_price_downloader.cli --tickers AAPL --interval 1m --period 1d
```

### Python Library Usage

```python
from stock_price_downloader import StockConfig, StockDataDownloader
from stock_price_downloader.config import TimeInterval

# Create configuration
config = StockConfig(
    tickers=["AAPL", "MSFT"],
    interval=TimeInterval.DAILY,
    period="1y",
    output_dir="data"
)

# Download data
downloader = StockDataDownloader(config)
downloader.download_all()
```

## Configuration

The package supports the following configuration options:

- `tickers`: List of stock tickers to download
- `interval`: Time interval for the data (1d, 1h, or 1m)
- `period`: Time period to download (e.g., "1y", "1mo", "1d")
- `output_dir`: Directory where JSON files will be saved

## Output Format

The downloaded data is saved in JSON format with the following structure:

```json
{
  "ticker": "AAPL",
  "interval": "1d",
  "period": "1y",
  "data": [
    {
      "Date": "2023-01-01",
      "Open": 100.0,
      "High": 101.0,
      "Low": 99.0,
      "Close": 100.5,
      "Volume": 1000000
    },
    ...
  ]
}
```

## License

MIT
