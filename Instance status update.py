import boto3
import os

sns_client = boto3.client('sns')

# Read SNS Topic ARN from environment variable for flexibility
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:ca-central-1:975050024946:aviral_instance_notification')

def lambda_handler(event, context):
    """
    Triggered automatically by EventBridge when an EC2 instance changes state.
    Sends an SNS notification with instance ID and new state.
    """
    try:
        # Extract details from event
        detail = event.get('detail', {})
        instance_id = detail.get('instance-id')
        state = detail.get('state')

        if not instance_id or not state:
            print("Event missing instance-id or state:", event)
            return {"status": "error", "message": "Invalid event format"}

        # Prepare the message
        subject = f"EC2 Instance State Change: {state.upper()}"
        message = f"EC2 instance {instance_id} has changed state to: {state}"

        # Log the details for debugging
        print(f"Instance ID: {instance_id}")
        print(f"State: {state}")
        print("Publishing to SNS topic:", SNS_TOPIC_ARN)

        # Send notification
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )

        return {"status": "success", "instance_id": instance_id, "state": state}

    except Exception as e:
        print("Error processing event:", str(e))
        return {"status": "error", "message": str(e)}
