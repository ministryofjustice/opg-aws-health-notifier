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
