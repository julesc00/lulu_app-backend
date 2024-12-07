variable "region" {
  description = "AWS region"
  type        = string
}
variable "vpc_id" {
  description = "VPC ID to use"
  type        = string
}

variable "instance_ami" {
  description = "Ubuntu Linux instance, t2.micro."
  type        = string
}

variable "sg_id" {
  description = "IAM Security Group ID"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
}

variable "tf-state-bucket" {
  description = "S3 bucket to save terraform state on the cloud."
  type        = string
  default     = "briones-terraform-state"
}
variable "app_code" {
  description = "AppCode to identify the client's resources."
  type        = string
}
