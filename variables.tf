variable "account_name" {
  description = "AWS account name"
  type        = string
}

variable "ecr_repository_url" {
  type        = string
  description = "URL of the ECR repository"
}

variable "failed_invocation_sns_arn" {
  type        = string
  default     = ""
  description = "ARN of SNS Topic to send failed invocations to."
}

variable "slack_channel_id" {
  type        = string
  description = "Slack's internal ID for the channel you want to post messages, format AB1C2DEF"
}

variable "slack_secret_arn" {
  type        = string
  description = "Secret token for the aws notifier bot"
}

variable "version_tag" {
  type        = string
  description = "Tag of the AWS Health Notifier Image to Deploy"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}
