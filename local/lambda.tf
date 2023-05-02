module "aws_health_notifier" {
  source             = "../"
  account_name       = "opg-account"
  ecr_repository_url = aws_ecr_repository.health_notifier.repository_url
  slack_channel_id   = "123456"
  slack_secret_arn   = aws_secretsmanager_secret.aws_notifier_slack_token.arn
  version_tag        = "latest"
  providers = {
    aws           = aws
    aws.eu-west-2 = aws.eu-west-2
    aws.us-east-1 = aws.us-east-1
  }
}
