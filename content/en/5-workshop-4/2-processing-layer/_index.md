---
weight: 2
date: 2026-06-29
title: "Processing Layer"
chapter: false
pre: "<b>2.4.2. </b>"
---

After the raw data (JSON) has landed in the S3 Raw Bucket, we need a powerful engine to clean, flatten, and transform the data format to optimize storage costs.

In this chapter, we will use **AWS Glue** (running on an Apache Spark foundation) to perform this heavy lifting and write the output in **Parquet** columnar format.

{{% children %}}