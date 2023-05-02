resource "aws_ecr_repository" "health_notifier" {
  name     = "shared/aws-health-notifier"
  provider = aws.management
  image_scanning_configuration {
    scan_on_push = true
  }
}
