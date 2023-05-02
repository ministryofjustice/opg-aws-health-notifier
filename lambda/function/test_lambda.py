from send_health_events_to_slack import Message, blocks
import pytest

@pytest.fixture
def event():
    return {
    "version": "0",
    "id": "16337884-01d7-a8ba-0534-368fedf2f031",
    "detail-type": "AWS Health Event",
    "source": "aws.health",
    "account": "123456789",
    "time": "2022-12-15T23:25:00Z",
    "region": "eu-west-1",
    "resources": [
        "database-training-0",
    ],
    "detail": {
        "eventArn": "arn:aws:health:eu-west-1::event/RDS/AWS_RDS_OPERATIONAL_NOTIFICATION/AWS_RDS_OPERATIONAL_NOTIFICATION_228d6e2ee15b7b3adc7e7b7db05ea8ec67fc8ecb80853e74627821514df9a0b5",
        "service": "RDS",
        "eventTypeCode": "AWS_RDS_OPERATIONAL_NOTIFICATION",
        "eventTypeCategory": "accountNotification",
        "startTime": "Thu 15 Dec 2022 23: 25: 00 GMT",
        "eventDescription": [
            {
                "language": "en_US",
                "latestDescription": "We have a new operating system update available for one or more of your Aurora Serverless v2 instances in the EU-WEST-1 Region that contains critical stability fixes. We will automatically update your affected instances in the maintenance window over the 3 weeks following January 4, 2023 00:00 UTC. However, we recommend you manually apply the update at your earliest convenience. The instance(s) will be restarted once the update is applied. \n\nYour impacted Amazon Aurora database instances are listed in the \"Affected resources\" tab.\n\nRefer our documentation [1] to learn more about operating system updates. Reach out to your AWS account team or contact AWS Support [2] if you have any questions or require further guidance.\n\n[1] https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n[2] https://aws.amazon.com/support"
            }
            ],
        "affectedEntities": [
            {
                "entityValue": "database-training-0"
            }
        ]
    }
}

def test_message_class_base(event):
    message = Message(event)

    assert message.account == "123456789"
    assert message.region == "eu-west-1"
    assert message.url == "https://phd.aws.amazon.com/phd/home#/account/event-log?eventID=arn:aws:health:eu-west-1::event/RDS/AWS_RDS_OPERATIONAL_NOTIFICATION/AWS_RDS_OPERATIONAL_NOTIFICATION_228d6e2ee15b7b3adc7e7b7db05ea8ec67fc8ecb80853e74627821514df9a0b5"
    assert message.service == "RDS"
    assert message.description == "We have a new operating system update available for one or more of your Aurora Serverless v2 instances in the EU-WEST-1 Region that contains critical stability fixes. We will automatically update your affected instances in the maintenance window over the 3 weeks following January 4, 2023 00:00 UTC. However, we recommend you manually apply the update at your earliest convenience. The instance(s) will be restarted once the update is applied. \n\nYour impacted Amazon Aurora database instances are listed in the \"Affected resources\" tab.\n\nRefer our documentation [1] to learn more about operating system updates. Reach out to your AWS account team or contact AWS Support [2] if you have any questions or require further guidance.\n\n[1] https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n[2] https://aws.amazon.com/support"
    assert message.alert == False

def test_message_class_event_notification(event):
    message = Message(event)
    assert message.eventType == "Notification"

def test_message_class_event_issue(event):
    event["detail"]["eventTypeCategory"] = "issue"
    message = Message(event)
    assert message.eventType == "Issue"
    assert message.alert == True

def test_message_class_event_change(event):
    event["detail"]["eventTypeCategory"] = "scheduledChange"
    message = Message(event)
    assert message.eventType == "Scheduled Change"

def test_message_class_event_unknown(event):
    event["detail"]["eventTypeCategory"] = ""
    message = Message(event)
    assert message.eventType == "Unknown"

def test_message_class_event_absent(event):
    del event["detail"]["eventTypeCategory"]
    message = Message(event)
    assert message.eventType == "RDS"

def test_block_not_alert(event):
    message = Message(event)
    response = blocks(message)
    expected_response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "An event has occurred on the AWS Health Dashboard"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Event Type*: `Notification` *Service*: `RDS` \n*Account*: `123456789` *Region*: `eu-west-1`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "We have a new operating system update available for one or more of your Aurora Serverless v2 instances in the EU-WEST-1 Region that contains critical stability fixes. We will automatically update your affected instances in the maintenance window over the 3 weeks following January 4, 2023 00:00 UTC. However, we recommend you manually apply the update at your earliest convenience. The instance(s) will be restarted once the update is applied. \n\nYour impacted Amazon Aurora database instances are listed in the \"Affected resources\" tab.\n\nRefer our documentation [1] to learn more about operating system updates. Reach out to your AWS account team or contact AWS Support [2] if you have any questions or require further guidance.\n\n[1] https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n[2] https://aws.amazon.com/support"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Further details can be found on the <https://phd.aws.amazon.com/phd/home#/account/event-log?eventID=arn:aws:health:eu-west-1::event/RDS/AWS_RDS_OPERATIONAL_NOTIFICATION/AWS_RDS_OPERATIONAL_NOTIFICATION_228d6e2ee15b7b3adc7e7b7db05ea8ec67fc8ecb80853e74627821514df9a0b5|Health Dashboard>"
                }
            }
        ]
    assert response == expected_response

def test_block_alert(event):
    event["detail"]["eventTypeCategory"] = "issue"
    message = Message(event)
    response = blocks(message)
    expected_response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":alert: An event has occurred on the AWS Health Dashboard :alert:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Event Type*: `Issue` *Service*: `RDS` \n*Account*: `123456789` *Region*: `eu-west-1`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "We have a new operating system update available for one or more of your Aurora Serverless v2 instances in the EU-WEST-1 Region that contains critical stability fixes. We will automatically update your affected instances in the maintenance window over the 3 weeks following January 4, 2023 00:00 UTC. However, we recommend you manually apply the update at your earliest convenience. The instance(s) will be restarted once the update is applied. \n\nYour impacted Amazon Aurora database instances are listed in the \"Affected resources\" tab.\n\nRefer our documentation [1] to learn more about operating system updates. Reach out to your AWS account team or contact AWS Support [2] if you have any questions or require further guidance.\n\n[1] https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n[2] https://aws.amazon.com/support"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Further details can be found on the <https://phd.aws.amazon.com/phd/home#/account/event-log?eventID=arn:aws:health:eu-west-1::event/RDS/AWS_RDS_OPERATIONAL_NOTIFICATION/AWS_RDS_OPERATIONAL_NOTIFICATION_228d6e2ee15b7b3adc7e7b7db05ea8ec67fc8ecb80853e74627821514df9a0b5|Health Dashboard>"
                }
            }
        ]
    assert response == expected_response
