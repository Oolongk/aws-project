---
title: "Tầng Thu Thập (Ingestion Layer)"
date: 2026-06-29
weight: 10
chapter: true
pre: "<b>1. </b>"
---

# Tầng Thu Thập (Ingestion Layer)

Nhiệm vụ của tầng này là tự động hóa việc kết nối đến OpenDota API, lấy dữ liệu trận đấu dạng JSON nguyên bản (Raw) và đẩy thẳng vào vùng hạ cánh (Landing Zone) trên Amazon S3. 

Chúng ta sẽ thiết lập hạ tầng với tiêu chuẩn bảo mật khắt khe nhất (Least Privilege) trước khi viết Script thu thập dữ liệu.

{{% children %}}