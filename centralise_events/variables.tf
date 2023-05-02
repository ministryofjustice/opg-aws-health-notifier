variable "account_name" {
  description = "AWS account name"
}

variable "cross_region_event_bus_role" {
}

variable "primary_region_event_bus" {}

data "aws_region" "current" {}
