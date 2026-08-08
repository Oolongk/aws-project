---
weight: 3
date: "2026-05-13"
title: "System Testing & Verification"
chapter: false
pre: "<b>2.2.3. </b>"
---

#### Verifying System Operation

After building the entire Serverless infrastructure on AWS in Chapter 2, it's now time to connect everything together and activate the system.

In this chapter, we will:
1. Update security certificates in the Python source code and launch the simulated truck fleet.
2. Monitor real-time data flowing into the DynamoDB database.
3. Check the Email inbox to confirm the automated alerting system works accurately when the temperature exceeds the safety threshold.

This verification step confirms that our Data Pipeline (IoT Core ➔ SQS ➔ Lambda ➔ DynamoDB & SNS) is running smoothly.

#### Contents

1. [Run the truck simulator](1-run-simulator/)
2. [Verify results](2-verify-results/)