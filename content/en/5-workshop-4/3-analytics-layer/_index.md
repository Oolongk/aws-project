---
weight: 3
date: 2026-06-29
title: "Analytics Layer"
chapter: false
pre: "<b>2.4.3. </b>"
---

After data has been flattened and compressed into Parquet in Chapter 2, it is ready for analysis. However, instead of downloading data to a local machine for analysis, we will use **Amazon Athena** — AWS's extremely powerful Serverless SQL query service.

Athena allows you to write familiar SQL statements to query directly on files in S3 without needing to set up or manage any database servers. In this chapter, we will learn the **Partition Projection** technique to optimize query performance.

{{% children %}}