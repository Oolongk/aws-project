---
weight: 2
date: "2026-05-13"
title: "Verify Data Flow & Alerts"
chapter: false
pre: "<b>2.2.3.2. </b>"
---

#### 1. Inspect the DynamoDB Storage

As soon as the Python script is running, data is being pushed through IoT Core, into SQS, and written directly to the database by Lambda.

1. Return to the AWS Console and open **DynamoDB**.
2. Select **Explore items** from the left menu.
3. Select your `IoT_Fleet_Data` table.
4. Click the **Run** (or Scan) button. You will see a stream of records (Items) appear with complete information: `truck_id`, `temperature`, `latitude`, `longitude`, and `timestamp_ms`.

![DynamoDB data](/aws-project/images/IoTSentinel/3-kiem-tra/dynamo_data.png?featherlight=false&width=90pc)

*Data is updated continuously in real-time!*

#### 2. Check Emergency Alert Email

In the simulator source code, the temperature is set to fluctuate randomly. If any truck has a temperature exceeding **8.0°C**, the Lambda function will immediately trigger SNS.

1. Open your personal Email inbox (the Email registered in Lesson 2.1).
2. You will see alert emails arriving with the subject: **Vaccine Temperature Alert**.
3. The email content will specifically identify which truck is experiencing an issue and what the current temperature is.

![Alert email](/aws-project/images/IoTSentinel/3-kiem-tra/email_alert.png?featherlight=false&width=90pc)

---