import json
import os
import boto3
from datetime import datetime
from stock_price_downloader import StockDataDownloader, StockConfig, TimeInterval

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get S3 bucket from environment variable
    bucket_name = os.environ['S3_BUCKET']

    # Create configuration
    config = StockConfig(
        tickers=["AAPL", "MSFT", "GOOGL"],  # You can modify this list or get it from event
        interval=TimeInterval.DAILY,
        period="1y",
        output_dir="/tmp"  # Lambda only allows writing to /tmp
    )

    # Initialize downloader
    downloader = StockDataDownloader(config)

    # Get current date for directory structure
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Download data for all tickers
    for ticker in config.tickers:
        try:
            print(f"Downloading data for {ticker}...")
            data = downloader._download_stock_data(ticker)

            # Generate S3 key with date-based directory structure
            s3_key = f"{current_date}/{ticker}.json"

            # Upload to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json.dumps(data, indent=2, default=str)
            )
            print(f"Data uploaded to s3://{bucket_name}/{s3_key}")

        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Stock data download completed successfully!')
    }
