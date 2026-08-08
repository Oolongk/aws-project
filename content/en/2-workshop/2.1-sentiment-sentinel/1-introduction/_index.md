---
weight: 1
date: 2026-02-25
title: "Introduction"
chapter: false
pre: "<b>2.1.1. </b>"
---

### Project Introduction

This project builds a fully automated Serverless system that:

1. **Automatically collects** YouTube comments daily via the YouTube Data API v3.
2. **Analyzes sentiment** using Generative AI (Amazon Bedrock - Claude 3) with context and sarcasm understanding.
3. **Stores** results in Amazon S3 (Data Lake) and Amazon DynamoDB.
4. **Visualizes** insights through interactive dashboards on Amazon QuickSight.

### Core Architecture

The system follows a **Decoupled Event-Driven** architecture:

| Component | Service | Role |
|---|---|---|
| Data Collection | AWS Lambda (Producer) | Fetches YouTube video list by keyword |
| Message Queue | Amazon SQS | Buffers video IDs, preventing API overload |
| AI Processing | AWS Lambda (Consumer + Transformer) | Fetches comments and calls Bedrock for analysis |
| Data Storage | Amazon S3 + DynamoDB | Data Lake and deduplication tracking |
| Analytics | Amazon Athena + QuickSight | SQL queries and dashboard visualization |
| Automation | Amazon EventBridge | Triggers pipeline daily at 8:00 AM |

### Why This Architecture?

**Problem:** YouTube Data API v3 has a strict daily quota. Calling it in a single synchronous function risks timeouts and quota exhaustion.

**Solution:** Separate the workload into 3 Lambda functions connected via SQS queues:
- `Producer_Lambda` → fetches video list, pushes IDs to SQS
- `Consumer_Lambda` → reads from SQS, fetches comments, calls Bedrock
- `Transformer_Lambda` → reads raw S3 output, transforms into Athena-queryable Parquet