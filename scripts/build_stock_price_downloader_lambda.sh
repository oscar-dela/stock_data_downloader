#!/bin/bash
set -eux

cd ../stock_price_downloader
rm -rf dist package
poetry install --only main --sync
poetry build
poetry run pip install --upgrade -t package dist/*.whl
cd package; mkdir -p out; zip -r -q out/artifact.zip . -x '*.pyc'
mv out/artifact.zip ../../terraform/stock_price_downloader_lambda.zip
