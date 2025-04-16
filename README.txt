
AWS Basics Project - CSE546
Animesh Chaudhary 

Overview
This project automates the creation, interaction, and deletion of AWS resources using Python and the boto3 library. It creates an EC2 instance, S3 bucket, and SQS queue, uploads a file to S3, sends a message to SQS, and then deletes all the resources.

Running the Project
1. Executable File:  project1_main.py file.
2. Run the script in the terminal:
   python3 project1_main.py

The script will:
- Create an EC2 instance, S3 bucket, and SQS FIFO queue.
- Wait for 1 minute for the resources to be ready.
- List all resources.
- Upload a file to S3.
- Send a message to the SQS queue, retrieve, and delete it.
- Wait for 10 seconds, then delete all resources.
- Wait for 20 seconds and list resources to confirm deletion.


Video Demo
You can find a video demonstration.

Submission
Zip of the the project files (project1_main.py,CSE546test.txt, README, and video demo) is attached.
