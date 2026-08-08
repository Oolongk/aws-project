---
weight: 5
date: 2026-06-29
title: "API & UI Layer"
chapter: false
pre: "<b>2.4.5. </b>"
---

With aggregated metrics securely loaded into Amazon DynamoDB in Chapter 4, the final phase is building an API interface and web UI so users can query the data.

In this chapter, we establish a complete Serverless API architecture: using **AWS Lambda** as the Backend to query data from DynamoDB, fronted by **Amazon API Gateway** to process HTTP requests originating from the **Frontend Website** hosted on S3.

{{% children %}}