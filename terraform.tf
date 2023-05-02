terraform {
  required_version = ">= 1.4.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.7.0"
      configuration_aliases = [
        aws.eu-west-2,
        aws.us-east-1,
      ]
    }
  }
}
