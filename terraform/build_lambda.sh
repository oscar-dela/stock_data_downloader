#!/bin/bash

# Create a temporary directory
mkdir -p lambda_package

# Install dependencies
pip install -r ../stock_price_downloader/requirements.txt -t lambda_package/

# Copy the Lambda function
cp lambda_function.py lambda_package/

# Copy the stock price downloader package
cp -r ../stock_price_downloader/stock_price_downloader lambda_package/

# Create the zip file
cd lambda_package
zip -r ../stock_price_downloader.zip .
cd ..

# Clean up
rm -rf lambda_package
