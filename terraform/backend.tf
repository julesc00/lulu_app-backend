terraform {
  backend "s3" {
    bucket = "briones-terraform-state"
    key    = "luluapp/terraform.tfstate"
    region = "us-east-1"

  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}