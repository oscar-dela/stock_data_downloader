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
	cd terraform && \
	./build_lambda.sh
