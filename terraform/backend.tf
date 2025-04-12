terraform {
  backend "s3" {
    bucket         = "huaweic-tf-state"
    key            = "stock_price_downloader.tfstate"
    region         = "us-west-2"
    dynamodb_table = "huaweic-tf-lock"
  }
}
