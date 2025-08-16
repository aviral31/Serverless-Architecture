# Serverless-Architecture
This repository contains Python scripts and setup instructions for multiple **AWS Lambda assignments** designed to build hands-on DevOps skills with **EC2, S3, SNS, and EventBridge**. Each assignment demonstrates automation using **Boto3** (the AWS SDK for Python).

---

## Table of Contents

1. [Assignment 1: Automated EC2 Instance Management](#assignment-1-automated-ec2-instance-management)
2. [Assignment 2: Automated S3 Bucket Cleanup](#assignment-2-automated-s3-bucket-cleanup)
3. [Assignment 3: Monitor Unencrypted S3 Buckets](#assignment-3-monitor-unencrypted-s3-buckets)
4. [Assignment 4: Monitor EC2 Instance State Changes](#assignment-4-monitor-ec2-instance-state-changes)

---

## Assignment 1: Automated EC2 Instance Management

**Objective:** Automatically stop or start EC2 instances based on assigned tags.

### Steps:

1. **Setup EC2 Instances:**

   * Created two EC2 instances (`t2.micro`).
   * Tagged them:

     * `Action=Auto-Stop`
     * `Action=Auto-Start`

2. **IAM Role:**

   * Created a Lambda role.
   * Attached `AmazonEC2FullAccess` policy (restrict in production).

3. **Lambda Function:**

   * Used Boto3 to:

     * Find instances tagged `Auto-Stop` → stop them.
     * Find instances tagged `Auto-Start` → start them.
   * Logged affected instance IDs.

4. **Testing:**

   * Invoked the Lambda manually.
   * Verified instances start/stop correctly in the EC2 dashboard.

---

## Assignment 2: Automated S3 Bucket Cleanup

**Objective:** Automatically delete files older than 30 days in a specific S3 bucket.

### Steps:

1. **Setup S3 Bucket:**

   * Used a bucket named "aviralpaliwal3105".

2. **IAM Role:**

   * Created a Lambda role.
   * Attached `AmazonS3FullAccess` (use restrictive policy in production).

3. **Lambda Function:**

   * Used Boto3 to:

     * List objects in the bucket.
     * Compare `LastModified` date against current date.
     * Delete files older than 30 days.
     * Print names of deleted files.

4. **Testing:**

   * Invoked Lambda manually.
   * Confirmed only files <30 days remain in S3.

---

## Assignment 3: Monitor Unencrypted S3 Buckets

**Objective:** Detect S3 buckets without server-side encryption enabled.

### Steps:

1. **S3 Buckets:**

   * Checked this for all buckets in region "ca-central-1". Created some buckets with encryption disabled

2. **IAM Role:**

   * Created a Lambda role.
   * Attached `AmazonS3ReadOnlyAccess` policy.

3. **Lambda Function:**

   * Used Boto3 to:

     * List all buckets in ca-central-1.
     * Check bucket encryption settings.
     * Print names of buckets and their encryption status.

4. **Testing:**

   * Invoked Lambda manually.
   * Reviewed CloudWatch logs for detection results.

---

## Assignment 4: Monitor EC2 Instance State Changes

**Objective:** Monitor EC2 instance lifecycle events and send notifications when instances are started or stopped.

### Steps:

1. **SNS Setup:**

   * Created a new SNS topic.
   * Subscribed with my email to the topic.

2. **IAM Role:**

   * Created a Lambda role with:

     * `AmazonSNSFullAccess`

3. **Lambda Function:**

   * Used Boto3 to:

     * Extract `instance-id` and `state` from the incoming event.
     * Publish to SNS with instance details.

4. **EventBridge Rule:**

   * Created a rule with event pattern and defined it for two instances created by me:

     ```json
   {
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "instance-id": ["i-061465948878d6f02", "i-07025c962a68f9304"],
    "state": ["running", "stopped"]
  }
}
     ```
   * Target = Lambda function.

5. **Testing:**

   * Start or stop an EC2 instance.
   * Confirm email notification received via SNS.

---
