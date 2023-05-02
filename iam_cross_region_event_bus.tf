resource "aws_iam_role" "cross_region_event_bus" {
  name               = "cross-region-event-bus-${var.account_name}"
  assume_role_policy = data.aws_iam_policy_document.event_bridge_assume.json
  lifecycle {
    create_before_destroy = true
  }
}

data "aws_iam_policy_document" "event_bridge_assume" {
  statement {
    sid     = "AllowEventBridgeAssumeRole"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "send_events_to_primary_event_bus" {
  statement {
    sid       = "AllowSendEventsToPrimaryRegionEventBus"
    actions   = ["events:PutEvents"]
    effect    = "Allow"
    resources = [data.aws_cloudwatch_event_bus.primary.arn]
  }
}

resource "aws_iam_policy" "send_events_to_primary_event_bus" {
  name   = "send-to-cross-region-event-bus-${var.account_name}"
  policy = data.aws_iam_policy_document.send_events_to_primary_event_bus.json
}

resource "aws_iam_role_policy_attachment" "send_events_to_primary_event_bus" {
  role       = aws_iam_role.cross_region_event_bus.name
  policy_arn = aws_iam_policy.send_events_to_primary_event_bus.arn
}
