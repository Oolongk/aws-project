---
weight: 2
date: "2026-05-13"
title: "Cloud Infrastructure Deployment"
chapter: false
pre: "<b>2.2.2. </b>"
---

#### Deploy the System on AWS

In this chapter, we will start configuring the Serverless services on the **AWS Management Console**. Our deployment strategy follows a bottom-up approach, working from the end of the data flow back to the beginning:

1. **Storage & Alerting (DynamoDB, SNS)**: Prepare the journey data "storage" and set up the "loudspeaker" to send email notifications when incidents occur.
2. **Processing & Buffering (Lambda, SQS)**: Create a queue to buffer high-speed data, while writing a function to handle temperature checking logic.
3. **Ingestion (IoT Core)**: Create a virtual device (Thing), provision security certificates, and configure a Rule to route the data stream into the queue.

Deploying in this order allows services to easily identify and grant permissions to each other without encountering "resource not found" errors.

#### Contents

1. [Initialize DynamoDB & SNS](1-dynamodb-sns/)
2. [Configure SQS & Lambda](2-sqs-lambda/)
3. [Set Up IoT Core](3-iot-core/)