module "eu-west-2" {
  source                      = "./centralise_events"
  account_name                = var.account_name
  cross_region_event_bus_role = aws_iam_role.cross_region_event_bus
  primary_region_event_bus    = data.aws_cloudwatch_event_bus.primary
  providers = {
    aws = aws.eu-west-2
  }
}

module "us-east-1" {
  source                      = "./centralise_events"
  account_name                = var.account_name
  cross_region_event_bus_role = aws_iam_role.cross_region_event_bus
  primary_region_event_bus    = data.aws_cloudwatch_event_bus.primary
  providers = {
    aws = aws.us-east-1
  }
}
