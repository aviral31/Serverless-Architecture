import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all instances with 'Action=Auto-Stop'
    stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    stop_ids = []
    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        print(f"Stopping instances: {stop_ids}")
        ec2.stop_instances(InstanceIds=stop_ids)
    else:
        print("No instances to stop.")

    # Get all instances with 'Action=Auto-Start'
    start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    start_ids = []
    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        print(f"Starting instances: {start_ids}")
        ec2.start_instances(InstanceIds=start_ids)
    else:
        print("No instances to start.")

    return {
        'statusCode': 200,
        'body': f'Started: {start_ids}, Stopped: {stop_ids}'
    }
