---
weight: 4
date: 2026-07-06
title: "Serving Layer và Web Frontend"
chapter: false
pre: "<b>2.5.4. </b>"
---

Chương này đưa QMJ Parquet từ S3 Processed lên website bằng kiến trúc event-driven: S3 trigger Lambda QMJ Loader, Loader ghi DynamoDB, Lambda Reader query theo ticker, API Gateway trả JSON và Web Frontend vẽ Chart.js.

{{% children %}}