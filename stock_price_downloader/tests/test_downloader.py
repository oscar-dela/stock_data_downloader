import os
import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock

from stock_price_downloader.config import StockConfig, TimeInterval
from stock_price_downloader.downloader import StockDataDownloader


class TestStockDataDownloader(TestCase):
    def setUp(self):
        self.config = StockConfig(
            tickers=["AAPL", "GOOGL"],
            interval=TimeInterval.DAILY,
            period="1mo",
            output_dir="test_output"
        )
        self.downloader = StockDataDownloader(self.config)

    def tearDown(self):
        # Clean up test output directory
        if os.path.exists(self.config.output_dir):
            for file in os.listdir(self.config.output_dir):
                os.remove(os.path.join(self.config.output_dir, file))
            os.rmdir(self.config.output_dir)

    def test_initialization(self):
        """Test that the downloader is initialized correctly and output directory is created."""
        self.assertEqual(self.downloader.config, self.config)
        self.assertTrue(os.path.exists(self.config.output_dir))

    def test_format_filename(self):
        """Test that filenames are formatted correctly."""
        ticker = "AAPL"
        filename = self.downloader._format_filename(ticker)

        # Check if filename contains expected components
        self.assertIn(ticker, filename)
        self.assertIn(self.config.interval.value, filename)
        self.assertIn(".json", filename)

        # Check if timestamp is in correct format
        # The filename format is: {ticker}_{interval}_{timestamp}.json
        parts = filename.split("_")
        timestamp = parts[-1].replace(".json", "")
        try:
            datetime.strptime(timestamp, "%H%M%S")
        except ValueError:
            self.fail("Timestamp in filename is not in correct format")

    @patch('yfinance.Ticker')
    def test_download_stock_data(self, mock_ticker):
        """Test that stock data is downloaded and formatted correctly."""
        # Setup mock
        mock_data = MagicMock()
        mock_data.index = [
            datetime(2023, 1, 1),
            datetime(2023, 1, 2),
            datetime(2023, 1, 3)
        ]
        # Create a proper DataFrame mock
        mock_data.__len__.return_value = 3
        mock_data.iloc = MagicMock()
        mock_data.iloc.__getitem__.side_effect = [
            MagicMock(to_dict=lambda: {"Open": 100, "High": 101, "Low": 99, "Close": 100.5, "Volume": 1000}),
            MagicMock(to_dict=lambda: {"Open": 100.5, "High": 102, "Low": 100, "Close": 101, "Volume": 1100}),
            MagicMock(to_dict=lambda: {"Open": 101, "High": 103, "Low": 101, "Close": 102, "Volume": 1200})
        ]
        mock_ticker.return_value.history.return_value = mock_data

        # Test download
        data = self.downloader._download_stock_data("AAPL")

        # Verify data structure
        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["interval"], self.config.interval.value)
        self.assertEqual(data["period"], self.config.period)
        self.assertEqual(len(data["data"]), 3)

        # Verify first record
        first_record = data["data"][0]
        self.assertEqual(first_record["Open"], 100)
        self.assertEqual(first_record["High"], 101)
        self.assertEqual(first_record["Low"], 99)
        self.assertEqual(first_record["Close"], 100.5)
        self.assertEqual(first_record["Volume"], 1000)
        self.assertIn("start_time", first_record)
        self.assertIn("end_time", first_record)

    def test_save_data(self):
        """Test that data is saved correctly to a JSON file."""
        test_data = {
            "ticker": "AAPL",
            "interval": TimeInterval.DAILY.value,
            "period": "1mo",
            "data": [{"price": 100, "volume": 1000}]
        }

        filename = os.path.join(self.config.output_dir, "test.json")
        self.downloader._save_data(test_data, filename)

        # Verify file exists and contains correct data
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r") as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data, test_data)

    @patch('yfinance.Ticker')
    def test_download_all(self, mock_ticker):
        """Test the complete download process for all tickers."""
        # Setup mock
        mock_data = MagicMock()
        mock_data.index = [datetime(2023, 1, 1)]
        # Create a proper DataFrame mock
        mock_data.__len__.return_value = 1
        mock_data.iloc = MagicMock()
        mock_data.iloc.__getitem__.return_value = MagicMock(
            to_dict=lambda: {"Open": 100, "High": 101, "Low": 99, "Close": 100.5, "Volume": 1000}
        )
        mock_ticker.return_value.history.return_value = mock_data

        # Test download_all
        self.downloader.download_all()

        # Verify files were created for each ticker
        for ticker in self.config.tickers:
            files = [f for f in os.listdir(self.config.output_dir) if f.startswith(ticker)]
            self.assertTrue(len(files) > 0, f"No files found for ticker {ticker}")

            # Verify file content
            with open(os.path.join(self.config.output_dir, files[0]), "r") as f:
                data = json.load(f)
                self.assertEqual(data["ticker"], ticker)
                self.assertEqual(len(data["data"]), 1)
