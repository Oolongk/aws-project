---
weight: 5
date: 2026-07-06
title: "Automation và Observability"
chapter: false
pre: "<b>2.5.5. </b>"
---

EventBridge Scheduler chỉ trigger Daily Ingestion. Không đưa Glue Workflow vào project vì hiện tại chưa có workflow code/configuration. Transform và Publisher chạy tách để tránh mô tả dependency không tồn tại.

{{% children %}}