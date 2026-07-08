---
title: "1. Giới thiệu và Kiến trúc"
date: 2026-02-25
weight: 1
---

## Bài toán đặt ra
Các thương hiệu cần hiểu khách hàng nói gì về họ trên mạng xã hội. Việc đọc thủ công hàng ngàn comment là bất khả thi, và các công cụ truyền thống không hiểu được sự "châm biếm" (Sarcasm).

## Kiến trúc Serverless (Event-Driven)

Hệ thống được thiết kế theo mô hình **Event-Driven Architecture** với 3 tầng chính:

1.  **Ingestion Layer:** Thu thập dữ liệu thô.
2.  **AI Processing Layer:** Xử lý và phân tích bằng AI.
3.  **Serving & BI Layer:** Truy vấn và hiển thị.

![Sơ đồ kiến trúc hệ thống](/images/sentinel/architecture_diagram.png)
    

### Điểm nhấn công nghệ
* **AWS Lambda:** Chạy code Python serverless.
* **Amazon Bedrock (Claude 3):** Trí tuệ nhân tạo để đọc hiểu ngôn ngữ tự nhiên.
* **Amazon S3:** Data Lake lưu trữ dữ liệu.
* **Kỹ thuật "Traffic Cop":** Kiểm soát luồng dữ liệu để tránh sập API.