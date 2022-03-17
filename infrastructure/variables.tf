variable "aws_region" {
  default = "us-east-1"
}

variable "lambda_function_name" {
  default = "RAISexecutaEMR"
}

variable "key_pair_name" {
  default = "eric-igti-teste"
}

variable "airflow_subnet_id" {
  default = "subnet-023bffa8b7a996029"
}

variable "vpc_id" {
  default = "vpc-049efbdc9209d321b"
}
