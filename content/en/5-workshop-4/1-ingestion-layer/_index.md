---
weight: 1
date: 2026-06-29
title: "Ingestion Layer"
chapter: false
pre: "<b>2.4.1. </b>"
---

The responsibility of this layer is to automate the connection to the OpenDota API, retrieve raw match data in JSON format, and push it directly into the Landing Zone on Amazon S3.

We will set up the infrastructure with the strictest security standards (Least Privilege) before writing the data ingestion script.

{{% children %}}