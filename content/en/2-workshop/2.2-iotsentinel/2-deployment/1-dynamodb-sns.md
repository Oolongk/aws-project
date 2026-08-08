---
weight: 1
date: "2026-05-13" 
title: "Create DynamoDB & Configure Amazon SNS"
chapter: false
pre: "<b>2.2.2.1. </b>"
---

#### 1. Initialize Amazon DynamoDB storage

Amazon DynamoDB is a NoSQL database with response times in milliseconds, extremely suitable for storing continuous time-series data streaming from trucks.

1. Access the **AWS Management Console**, search for and open **DynamoDB**.
2. In the left menu, select **Tables** and click the **Create table** button.
3. Configure the table with the following parameters:
   - **Table name**: `IoT_Fleet_Data`
   - **Partition key**: `truck_id` (Type: **String**) - *Used to group data by each truck.*
   - **Sort key**: `timestamp_ms` (Type: **Number**) - *Used to sort journey data in real-time.*

![Create DynamoDB table](/aws-project/images/IoTSentinel/2-trien-khai/dynamodb-create.png?featherlight=false&width=90pc)

4. In the **Table settings** section, keep the **Default settings** option.
![Create DynamoDB table](/aws-project/images/IoTSentinel/2-trien-khai/dynamodb-create-2.png?featherlight=false&width=90pc)

5. Scroll down to the bottom and click **Create table**. The creation process will take a few seconds.

![DynamoDB Success](/aws-project/images/IoTSentinel/2-trien-khai/dynamodb_success.png?featherlight=false&width=90pc)

---

#### 2. Initialize Amazon SNS alert channel

Amazon Simple Notification Service (SNS) will help us send immediate notifications to the manager's Email when AWS Lambda detects that the truck's temperature exceeds the allowable limit.

1. Search for and open the **Simple Notification Service (SNS)**.
2. In the left menu, select **Topics** and click **Create topic**.
3. On the Create Topic page, configure as follows:
   - **Type**: Select **Standard** *(Note: Standard is required because the FIFO type does not support sending Emails).*
   - **Name**: `TemperatureAlerts`

![Create SNS Topic](/aws-project/images/IoTSentinel/2-trien-khai/sns_topic.png?featherlight=false&width=90pc)

4. Scroll down to the bottom and click **Create topic**.

**Register Alert Email:**

After successfully creating the Topic, you will be redirected to that Topic's details page. Now, we need to declare the Email to receive notifications.

1. Click the **Create subscription** button.
2. Configure Subscription:
   - **Protocol**: Select **Email**.
   - **Endpoint**: Enter your real Email address (Example: `admin@gmail.com`).

![Create Subscription](/aws-project/images/IoTSentinel/2-trien-khai/sns_sub.png?featherlight=false&width=90pc)

3. Click **Create subscription**. The status will now be *Pending confirmation*.
4. **Verify Email**: Open your Email inbox, find the email with the subject *AWS Notification - Subscription Confirmation* and click the **Confirm subscription** link.

![Confirm Email](/aws-project/images/IoTSentinel/2-trien-khai/sns_confirm.png?featherlight=false&width=90pc)
![Confirm Email](/aws-project/images/IoTSentinel/2-trien-khai/sns_confirm_2.png?featherlight=false&width=90pc)
![Confirm Email](/aws-project/images/IoTSentinel/2-trien-khai/sns_confirm_3.png?featherlight=false&width=90pc)