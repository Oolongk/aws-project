---
weight: 2
date: 2026-03-05
title: "Create IAM Role & Enable AI"
chapter: false
pre: "<b>2.1.2.2. </b>"
---

In AWS, services are isolated by default and are not permitted to communicate with each other. To allow Lambda to call AI Bedrock, read/write files on S3, and run Athena queries, we must grant it an identity card called an **IAM Role**.

Additionally, we need to "wake up" the Claude 3 model on Amazon Bedrock before using it in code.

---

## 1. Enable Amazon Bedrock (Claude 3 Haiku)

*Good news: Since 2026, AWS has simplified model permission granting to the maximum extent possible through the **Auto-enablement** mechanism at the account level!*

1. Log in to the AWS Console and ensure you are in the **N. Virginia (us-east-1)** or **Oregon (us-west-2)** Region.
2. Access the **Amazon Bedrock** service.
3. In the left menu, find **Playgrounds** and select **Chat** (or Text).
4. Click the **Select model** button -> Select provider **Anthropic** -> Select **Claude 3 Haiku**.
5. Type a test greeting (e.g., "Hello Claude") and click Send. AWS will automatically approve and activate the model for you instantly!

*(Note: If your account is brand new and AWS displays a form requesting **Submit use case details**, simply fill in: Project name, Website (can be a Github link), and Description as "Social media data analysis for educational purposes" then click Submit.)*

![Test Claude 3 on Playgrounds](/aws-project/images/youtube/2-Chuan-bi/bedrock-playgrounds-test.png)

---

## 2. Create IAM Role for Ingestor Lambda

The Ingestor function is responsible for scraping raw data and writing to the Data Lake (S3), while also marking records in DynamoDB.

1. Access **AWS IAM** -> Select **Roles** in the left menu -> Click **Create role**.
2. **Trusted entity type:** Select **AWS service**.
3. **Use case:** Select **Lambda** -> Click **Next**.
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-1.png)
4. In the search box (Permissions policies), find and **check 4 permissions**:
   * `AmazonS3FullAccess`
   * `AmazonDynamoDBFullAccess`
   * `AWSLambdaBasicExecutionRole` (Required permission to write activity logs)
   * `AmazonSQSFullAccess`
5. Click **Next** -> Name the Role `IngestorRole` -> Click **Create role**.
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-2.png)
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-3.png)
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-3-1.png)

---

## 3. Create IAM Role for Transformer Lambda

This function needs greater power to call AI and activate the Athena Data Catalog.

1. Repeat the Role creation steps from the section above (AWS service -> Lambda).
2. In the search box, find and **check 4 permissions**:
   * `AmazonS3FullAccess`
   * `AmazonBedrockFullAccess`
   * `AmazonAthenaFullAccess`
   * `AWSLambdaBasicExecutionRole`
3. Click **Next** -> Name the Role `TransformerRole` -> Click **Create role**.
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-4.png)
![Create IAM role](/aws-project/images/youtube/2-Chuan-bi/IAM-5.png)

![IAM Role created successfully](/aws-project/images/youtube/2-Chuan-bi/IAM-6.png)

**Security Best Practice:** In a production enterprise environment, we would not use `*FullAccess` permissions but instead write *Inline Policies* that limit access to a specific S3 Bucket. However, within the scope of this Data Pipeline practical exercise, using Managed Policies will help you avoid unnecessary "Access Denied" errors.