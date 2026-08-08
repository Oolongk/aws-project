---
weight: 4
date: "2026-05-13"
title: "Resource Cleanup"
chapter: false
pre: "<b>2.2.4. </b>"
---

#### Resource Cleanup

#### 1. Delete AWS IoT Core Configuration
1. Access **IoT Core** > **Manage** > **All devices** > **Things**.
2. Select `Vaccine_Truck_Fleet` and click **Delete**.
3. Go to **Message routing** > **Rules**, select `IoT_To_SQS_Rule` and click **Delete**.

![Delete IoT resources](/aws-project/images/IoTSentinel/4-don-dep/IoT-1.png?featherlight=false&width=90pc)
![Delete IoT resources](/aws-project/images/IoTSentinel/4-don-dep/IoT-2.png?featherlight=false&width=90pc)
![Delete IoT resources](/aws-project/images/IoTSentinel/4-don-dep/IoT-3.png?featherlight=false&width=90pc)

#### 2. Delete the Lambda Processor & SQS Queue
1. Open the **Lambda** service > **Functions**, select `IoT_Process_Data` and click **Delete**.

![Delete Lambda and SQS](/aws-project/images/IoTSentinel/4-don-dep/Lambda-1.png?featherlight=false&width=90pc)
![Delete Lambda and SQS](/aws-project/images/IoTSentinel/4-don-dep/Lambda-2.png?featherlight=false&width=90pc)

2. Open the **SQS** service > **Queues**, select `IoT_Fleet_Queue` and click **Delete**. Enter `confirm` in the confirmation box.

![Delete Lambda and SQS](/aws-project/images/IoTSentinel/4-don-dep/SQS-1.png?featherlight=false&width=90pc)

#### 3. Delete DynamoDB Database & SNS Notification
1. Open the **DynamoDB** service > **Tables**, select the `IoT_Fleet_Data` table and click **Delete**. Enter `confirm` to confirm.

![Delete DynamoDB and SNS](/aws-project/images/IoTSentinel/4-don-dep/Dynamodb-1.png?featherlight=false&width=90pc)
![Delete DynamoDB and SNS](/aws-project/images/IoTSentinel/4-don-dep/Dynamodb-2.png?featherlight=false&width=90pc)


2. Open the **SNS** service > **Topics**, select `TemperatureAlerts` and click **Delete**.

![Delete DynamoDB and SNS](/aws-project/images/IoTSentinel/4-don-dep/SNS-1.png?featherlight=false&width=90pc)
![Delete DynamoDB and SNS](/aws-project/images/IoTSentinel/4-don-dep/SNS-2.png?featherlight=false&width=90pc)

---

#### Project Summary

Through this Lab, you have mastered how to build a complete **Data Pipeline** flow:
- **Edge device setup**: Used Python to simulate truck journey data.
- **Data collection**: Used IoT Core and the MQTT protocol.
- **Buffering & Processing**: Used SQS to buffer data and Lambda to handle real-time logic.
- **Storage & Alerting**: Used DynamoDB for persistent storage and SNS for urgent email notifications.