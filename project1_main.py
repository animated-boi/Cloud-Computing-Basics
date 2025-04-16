import boto3
import time

# Create a session using your AWS credentials
session = boto3.Session(region_name='us-east-1')  

# Initialize clients
ec2 = session.client('ec2')
s3 = session.client('s3')
sqs = session.client('sqs')

# ----------------------------- Creating EC2 Instance -----------------------------
def create_ec2_instance():
    print("Creating EC2 instance...\n")
    response = ec2.run_instances(
        ImageId='ami-0e86e20dae9224db8',   
        InstanceType='t2.micro',
        KeyName='animesh-cc-project1-key-pair',  
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance created with Instance ID: {instance_id}\n")
    return instance_id

# ----------------------------- Creating S3 Bucket -----------------------------
def create_s3_bucket():
    bucket_name = 'animesh-cc-project1-s3-bucket'  
    print("Creating S3 bucket...\n")
    s3.create_bucket(
        Bucket=bucket_name
    )
    print(f"S3 bucket created with name: {bucket_name}\n")
    return bucket_name

# ----------------------------- Creating SQS Queue -----------------------------

def create_sqs_queue():
    print("Creating SQS FIFO queue...")
    response = sqs.create_queue(
        QueueName='animesh-cc-project1-sqs-queue.fifo',  
        Attributes={
            'FifoQueue': 'true',
            'ContentBasedDeduplication': 'true'
        }
    )
    queue_url = response['QueueUrl']
    print(f"SQS queue created with URL: {queue_url}")
    return queue_url

# ----------------------------- Wait for Resources -----------------------------
def wait_for_resources():
    print("\nRequest sent, wait for 1 minute...")
    time.sleep(60)  # Wait for 1 minute

# ----------------------------- Listing EC2, S3, SQS -----------------------------
def list_resources():
    print("\nListing EC2 instances:")
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']} - State: {instance['State']['Name']}")

    print("\nListing S3 buckets:")
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"Bucket Name: {bucket['Name']}\n")

    print("\nListing SQS queues:")
    response = sqs.list_queues()
    if 'QueueUrls' in response:
        for queue_url in response['QueueUrls']:
            print(f"Queue URL: {queue_url}\n")
    else:
        print("No SQS queues found.\n")

# ----------------------------- Uploading File to S3 -----------------------------
def upload_to_s3(bucket_name):
    file_name = 'CSE546test.txt'
    with open(file_name, 'w') as f:
        f.write('')

    print(f"Uploading {file_name} to S3 bucket...\n")
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}'\n")
    time.sleep(10)

# ----------------------------- Sending Message to SQS -----------------------------
def send_message_to_sqs(queue_url):
    print("Sending message to SQS queue...\n")
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody='This is a test message',
        MessageGroupId='testGroup1'  # Required for FIFO queues
    )
    print("Message sent to SQS queue.\n")
    time.sleep(10)
    

# ----------------------------- Retrieving and Deleting Message from SQS -----------------------------
def retrieve_and_delete_message(queue_url):
    print("Retrieving and deleting message from SQS queue...\n")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All']
    )

    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        print(f"Message Body: {message['Body']}\n")

        # Now delete the message
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from SQS queue.\n")
    else:
        print("No messages found in the queue.\n")

# ----------------------------- Deleting Resources -----------------------------
def delete_resources(instance_id, bucket_name, queue_url):
    # Terminate EC2 instance
    print(f"Terminating EC2 instance {instance_id}...\n")
    ec2.terminate_instances(InstanceIds=[instance_id])

    # Empty and delete S3 bucket
    print(f"Emptying and deleting S3 bucket {bucket_name}...\n")
    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()

    # Delete SQS queue
    print(f"Deleting SQS queue {queue_url}...\n")
    sqs.delete_queue(QueueUrl=queue_url)

    print("All resources deleted.\n")

# ----------------------------- Main Program -----------------------------
def main():
    # Step 1: Create resources
    ec2_instance_id = create_ec2_instance()
    s3_bucket_name = create_s3_bucket()
    sqs_queue_url = create_sqs_queue()

    # Step 2: Wait for resources to be ready
    wait_for_resources()

    # Step 3: List resources
    list_resources()

    # Step 4: Upload file to S3
    upload_to_s3(s3_bucket_name)

    # Step 5: Send message to SQS
    send_message_to_sqs(sqs_queue_url)

    # Step 6: Retrieve and delete message from SQS
    retrieve_and_delete_message(sqs_queue_url)

    # Step 7: Wait 10 seconds.
    time.sleep(10)

    # Step 8: Delete all resources
    delete_resources(ec2_instance_id, s3_bucket_name, sqs_queue_url)
    time.sleep(10)
    # Step 9: Wait 20 seconds and list resources again
    print("Waiting for 20 seconds...\n")
    time.sleep(30)
    list_resources()
    print("Here we can see that the sqs queue still appears but it's actually deleted, just that it takes some time to reflect...\n") 

# Run the main program
if __name__ == '__main__':
    main()

