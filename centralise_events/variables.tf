variable "account_name" {
  description = "AWS account name"
  type        = string
}

variable "cross_region_event_bus_role" {
  description = "Cross region event bus IAM role"
  type = object({
    arn  = string
    name = string
  })
}

variable "primary_region_event_bus" {
  description = "Primary region event bus"
  type = object({
    arn  = string
    name = string
  })
}

data "aws_region" "current" {}
