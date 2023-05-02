data "aws_cloudwatch_event_bus" "secondary" {
  name = "default"
}

resource "aws_cloudwatch_event_rule" "send_to_primary_event_bus" {
  name           = "send-aws-health-events-to-primary-region-event-bus"
  description    = "Send AWS Health Events to Primary Region for ${var.account_name}"
  event_bus_name = data.aws_cloudwatch_event_bus.secondary.name

  event_pattern = jsonencode(
    {
      "source" : ["aws.health"]
    }
  )
}

resource "aws_cloudwatch_event_target" "primary_event_bus" {
  arn       = var.primary_region_event_bus.arn
  role_arn  = var.cross_region_event_bus_role.arn
  rule      = aws_cloudwatch_event_rule.send_to_primary_event_bus.name
  target_id = "${var.account_name}-${data.aws_region.current.name}-send-to-primary-event-bus"
}
