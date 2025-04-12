terraform-init:
	cd terraform && \
    terraform init

terraform-plan:
	cd terraform && \
    terraform plan -out=tfplan

terraform-apply:
	cd terraform && \
    terraform apply tfplan

build-lambda:
	cd scripts && \
	./build_stock_price_downloader_lambda.sh
