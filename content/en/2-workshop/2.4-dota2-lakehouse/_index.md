---
weight: 4
title: "Building a Serverless Data Lakehouse: Dota 2 Meta Analytics"
date: 2026-06-29
chapter: true
pre: "<b>2.4. </b>"
---

# Introduction: Dota 2 Meta Analytics Data Lakehouse

Dota 2 is not only a billion-dollar eSports title with the world's most prestigious tournament (The International), but behind it lies a **massive Big Data goldmine**. Every second, millions of movement decisions, skill usages, and item purchases by professional players are systematically recorded.

**Problem Statement:** *How can we collect hundreds of thousands of complex JSON files from an API, clean them, and analyze which "Meta" (which Heroes or items currently have the highest win rate) to serve players for real-time lookup... without "burning through" server maintenance costs?*

This project is the answer. It guides you step-by-step in building a **100% Serverless Data Lakehouse** on AWS. By rigorously applying **FinOps (cloud cost optimization)** and **Decoupling (architecture separation)** principles, this system can process massive amounts of data at a cost approaching... zero!

---

## System Architecture

This project is designed to Enterprise architecture standards, clearly divided into 4 independent layers (Swimlanes). This separation ensures that if one layer fails (e.g., the API goes down), the other layers continue to operate normally (Fault Tolerance).

![Dota 2 Serverless Data Pipeline](/aws-project/images/dota2/Dota2-Pipeline.png?featherlight=false&width=90pc)

### Data Flow Details:

**1. Ingestion & Automation Layer**
* **Action:** Uses **AWS Lambda** (triggered daily via **EventBridge Cron**) to call the OpenDota API.
* **Result:** Fetches professional match data in `JSON` format and ingests directly into **Amazon S3 (Raw Zone)**. Data is partitioned by the standard `dt=YYYY-MM-DD` from the start.

**2. Processing / ETL Layer**
* **Action:** S3 Event Notifications automatically trigger **AWS Glue (PySpark)** jobs upon new file arrival.
* **Result:** Glue jobs parse JSON, flatten 10-player data arrays into tabular schemas, and output Snappy-compressed `Parquet` files to **Amazon S3 (Processed Zone)**.

**3. Analytics Layer**
* **Action:** Configures **Amazon Athena** for data engineers to run ad-hoc SQL queries on S3 Processed data.
* **Optimization:** Implements **Partition Projection** in Athena instead of Glue Crawlers, accelerating query execution and minimizing scanning costs.

**4. Serving & API Layer**
* **Action:** AWS Glue calculates aggregated metrics (Winrate, Pickrate) and upserts them directly into **Amazon DynamoDB**.
* **Serving the UI:** When a user accesses a static Web page (hosted on S3 Static Hosting), the Web calls HTTP API Gateway → Lambda Backend → Reads DynamoDB and returns results (latency below 100ms).
* **FinOps Strategy:** Static data such as hero images, item names, and skill descriptions are not stored in the Data Lake to reduce costs. The Frontend fetches them directly from the game's library API (Direct Fetch).

---

## What Will You Learn From This Project?

Upon completing this series, you will master the practical skills of a **Modern Data Engineer**:

1. **Serverless Orchestration:** Connect Lambda, S3, Glue, and EventBridge into a fully automated pipeline without managing a single server.
2. **PySpark ETL:** Perform complex data transformations (Flattening Arrays) and apply the Parquet compression standard.
3. **Advanced Athena:** Master the Partition Projection technique.
4. **Cloud Security & FinOps:** Apply Least Privilege IAM Roles and cost optimization strategies (Pay-per-request DynamoDB, Parquet Snappy Compression).


{{% children %}}