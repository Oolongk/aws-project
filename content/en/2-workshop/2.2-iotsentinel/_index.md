---
weight: 2
pre: "<b>2.2. </b>"
title: "IoT Fleet Monitoring System"
date: 2026-05-13
chapter: false
---

## The Problem
In the medical transport (vaccines) or frozen food industry, maintaining a stable temperature is a matter of survival. Manual monitoring is impossible with thousands of moving trucks, and just one cooling system failure can cause massive losses.

## Serverless Architecture (Event-Driven)

The system is designed following the **Event-Driven Architecture** model with 3 main layers:

1.  **Ingestion Layer:** Collects real-time GPS and temperature data from IoT devices on the trucks.
2.  **Processing & Buffering Layer:** Buffers the massive data stream and automatically processes logic to detect anomalies.
3.  **Storage & Alerting Layer:** Stores time-series data and triggers emergency alerts.

![System Architecture Diagram](/aws-project/images/IoTSentinel/IoT-Sentinel-Diagram.png)

### Technology Highlights
* **AWS IoT Core:** A secure gateway that receives MQTT data from thousands of devices.
* **Amazon SQS:** A "Shock absorber" (Buffer) that aggregates data, preventing system overload.
* **AWS Lambda:** Runs serverless Python code to process logic without managing servers.
* **Amazon DynamoDB:** A NoSQL Database that stores journey data at super high speed.
* **Amazon SNS:** Pushes emergency alerts via Email when the temperature exceeds the threshold.