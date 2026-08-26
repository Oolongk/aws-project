---
weight: 4
date: 2026-06-29
title: "Serving Layer"
chapter: false
pre: "<b>2.4.4. </b>"
---

Analyzed data, no matter how valuable, becomes useless if the system takes several minutes to display it to the user.

In this chapter, we will build a **Speed Layer** for the system using the NoSQL database **Amazon DynamoDB**. After cleaning the data, AWS Glue PySpark directly calculates the Meta metrics (Aggregated Metrics) and loads them straight into DynamoDB, ensuring the Frontend application can query information with sub-100ms latency.

{{% children %}}