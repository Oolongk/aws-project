---
weight: 1
date: "2026-05-13" 
title: "Environment and Simulator Preparation"
chapter: false
pre: "<b>2.2.1. </b>"
---

#### Preparation Steps

To build a real-time truck monitoring system, we need to prepare a simulated "data source" and set up the programming environment on a personal computer. Since we don't have real hardware devices, we will use Python to simulate 10 smart trucks.

- **Python & AWSIoTPythonSDK**: This is the main toolkit to turn your computer into an IoT Edge device. This library helps securely connect to the AWS Cloud via the MQTT protocol, encrypt data, and send temperature information.

- **AWS Region (Singapore - ap-southeast-1)**: To optimize speed and cost, we will consistently deploy all resources in the Singapore region. Choosing the right Region from the beginning helps services like SQS, Lambda, and DynamoDB connect with each other automatically and securely.

Thorough preparation of the simulated environment is an important stepping stone so the data stream can flow smoothly into the Pipeline in the subsequent steps.

#### Contents

1. [Setup Python Environment](1.1-setup-python/)
2. [Truck Simulator Source Code](1.2-code/)