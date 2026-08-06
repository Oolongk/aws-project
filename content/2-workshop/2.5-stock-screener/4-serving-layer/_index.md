---
title: "Chương 4. Serving Layer và Web Frontend"
date: 2026-07-06
weight: 4
chapter: true

---

Chương này đưa QMJ Parquet từ S3 Processed lên website bằng kiến trúc event-driven: S3 trigger Lambda QMJ Loader, Loader ghi DynamoDB, Lambda Reader query theo ticker, API Gateway trả JSON và Web Frontend vẽ Chart.js.

{{% children %}}
