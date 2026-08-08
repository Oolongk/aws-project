---
weight: 3
title: "Building an AI-Driven Serverless Data Lakehouse for Clickstream"
date: 2026-06-25
chapter: false
pre: "<b>2.3. </b>"
---


## Problem Statement
In the digital age, understanding user (reader) behavior in real time is the key to survival for electronic newspaper platforms. Processing massive clickstream data (unstructured JSON) requires a fully automated system from data ingestion, compression, and transformation (ETL) to feeding it into an AI model for personalized article recommendations, while optimizing operational costs close to $0.

## Serverless Architecture (Event-Driven)

The system is designed following the **Event-Driven Architecture** and Zero-ETL architecture with 3 main processing layers:

1. **Ingestion Layer:** Collects real-time clickstream data from an emulator and automatically compresses it on-the-fly from JSON to columnar format (Parquet).
2. **Orchestration & ETL Layer:** Orchestrates the entire workflow, completely resolving "Race Condition" errors between services, and invokes Serverless SQL to transform data into standard formats for AI.
3. **Storage & AI Layer:** Stores massive amounts of data on a Data Lake and trains an Artificial Intelligence model (Recommender System) with a strict cost management strategy.

![Clickstream system architecture diagram](/aws-project/images/Clickstream/Clicksteam-Diagram.png?featherlight=false&width=90pc)

### Technology Highlights
* **Amazon Kinesis Data Firehose:** A gateway that receives streaming data and directly converts JSON to Parquet based on the AWS Glue Schema.
* **AWS Step Functions:** The "conductor" that orchestrates the entire workflow, perfectly handling Data Latency and Race Condition issues using Wait States.
* **AWS Lambda & Amazon Athena:** Handles Serverless ETL logic to transform data extremely fast without maintaining servers.
* **Amazon S3:** Physical storage repository (Data Lake) containing Parquet and CSV files.
* **Amazon Personalize:** Automated machine learning model (AutoML) for recommending articles, combined with an ultra-saving FinOps "Hit and Run" strategy.

---

## Contents

{{% children %}}