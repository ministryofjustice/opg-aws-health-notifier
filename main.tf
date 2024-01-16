resource "aws_cloudwatch_event_rule" "health_events" {
  name           = "capture-health-events"
  description    = "Capture Health Events For ${var.account_name}"
  event_bus_name = data.aws_cloudwatch_event_bus.primary.name
  event_pattern = jsonencode(
    {
      "source" : ["aws.health"]
    }
  )
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.health_events.name
  target_id = "send-health-events-to-slack-${var.account_name}"
  arn       = aws_lambda_function.lambda_function.arn
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/send-health-events-to-slack-${var.account_name}"
  kms_key_id        = aws_kms_key.cloudwatch.arn
  retention_in_days = 400
}

resource "aws_lambda_function" "lambda_function" {
  function_name = "send-health-events-to-slack-${var.account_name}"
  image_uri     = "${var.ecr_repository_url}:${var.version_tag}"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 60
  depends_on    = [aws_cloudwatch_log_group.lambda]
  environment {
    variables = {
      SLACK_CHANNEL   = var.slack_channel_id
      SLACK_TOKEN_ARN = var.slack_secret_arn
    }
  }
  tracing_config {
    mode = "Active"
  }
}

resource "aws_cloudwatch_metric_alarm" "failed_invocation" {
  count             = var.failed_invocation_sns_arn != null ? 1 : 0
  alarm_actions     = [var.failed_invocation_sns_arn]
  alarm_description = "Health Notificatier Lambda Errors"
  alarm_name        = "health-notifier-lambda-errors"
  depends_on = [
    aws_lambda_function.lambda_function
  ]

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Average"
  threshold           = 0

  dimensions = {
    FunctionName = "${aws_lambda_function.lambda_function.function_name}"
  }
}
