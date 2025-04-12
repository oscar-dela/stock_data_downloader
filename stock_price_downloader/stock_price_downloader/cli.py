import argparse

from .config import StockConfig, TimeInterval
from .downloader import StockDataDownloader


def parse_args():
    parser = argparse.ArgumentParser(description="Download historical stock prices")
    parser.add_argument(
        "--tickers",
        nargs="+",
        help="List of stock tickers to download",
        required=True
    )
    parser.add_argument(
        "--interval",
        choices=[i.value for i in TimeInterval],
        default=TimeInterval.DAILY.value,
        help="Time interval for the data (default: 1d)"
    )
    parser.add_argument(
        "--period",
        default="1y",
        help="Time period to download (default: 1y)"
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Output directory for the JSON files (default: data)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    config = StockConfig(
        tickers=args.tickers,
        interval=TimeInterval(args.interval),
        period=args.period,
        output_dir=args.output_dir
    )

    downloader = StockDataDownloader(config)
    downloader.download_all()


if __name__ == "__main__":
    main()
