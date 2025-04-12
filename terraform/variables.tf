variable "region" {
  description = "The AWS region to deploy the resources in"
  type        = string
  default     = "us-west-2"
}

variable "project_prefix" {
  description = "The prefix for the project"
  type        = string
  default     = "draupnir"
}
