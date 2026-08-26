---
weight: 2
date: 2026-06-25
title: "Ingestion Layer"
chapter: false
pre: "<b>2.3.2. </b>"
---

After completing the infrastructure preparation, we move on to configuring the ingestion layer. 

The task of this layer is to catch raw JSON data from user devices, leverage the AWS Glue Schema created in Chapter 1 to compress the data on-the-fly (directly on the running stream) into Parquet, and securely store it down to the Amazon S3 Data Lake.
#### Contents
{{% children %}}