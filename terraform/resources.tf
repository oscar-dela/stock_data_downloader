# S3 bucket for storing stock data
resource "aws_s3_bucket" "stock_data" {
  bucket = "${var.project_prefix}-stock-price-data"
  force_destroy = true
}

# IAM role for Lambda
resource "aws_iam_role" "stock_price_downloader_lambda_role" {
  name = "stock_price_downloader_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for Lambda to write to S3
resource "aws_iam_role_policy" "stock_price_downloader_lambda_s3_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.stock_price_downloader_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.stock_data.arn,
          "${aws_s3_bucket.stock_data.arn}/*"
        ]
      }
    ]
  })
}

# Lambda function
resource "aws_lambda_function" "stock_price_downloader" {
  filename         = "stock_price_downloader_lambda.zip"
  function_name    = "stock_price_downloader"
  role             = aws_iam_role.stock_price_downloader_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 300
  memory_size      = 256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.stock_data.id
    }
  }
}

# CloudWatch Logs permissions
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.stock_price_downloader_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
