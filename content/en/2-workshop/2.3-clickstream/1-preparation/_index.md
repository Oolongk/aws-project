---
weight: 1
date: 2026-06-25
title: "Resource Preparation"
chapter: false
pre: "<b>2.3.1. </b>"
---

Before building the Data Pipeline, we need to prepare the foundational "ingredients" on the AWS cloud. 

This chapter will guide you through initializing 3 core components:
1. **Physical storage (Amazon S3):** Where the Data Lake data is stored.
2. **Data mold (AWS Glue Schema):** Defines the structure to compress JSON to Parquet.
3. **Notification channel (Amazon SNS):** Sets up an automated system for sending Email reports.

Preparing these resources well will help the architectural assembly steps in subsequent chapters run smoothly and avoid dependencies errors.
#### Contents
{{% children %}}