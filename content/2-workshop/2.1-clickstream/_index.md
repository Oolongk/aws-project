---
title: "Clickstream Analytics & AI Recommender"
date: 2026-07-08
weight: 4
chapter: true
pre: "Project 4 "
---

=======
# Clickstream Analytics & AI Recommender

## Bài toán đặt ra
Trong kỷ nguyên số, việc thấu hiểu hành vi người dùng (độc giả) theo thời gian thực chính là chìa khóa sống còn của các nền tảng báo điện tử. Việc xử lý luồng dữ liệu clickstream khổng lồ (dạng JSON phi cấu trúc) đòi hỏi một hệ thống tự động hóa hoàn toàn từ khâu thu thập, nén, biến đổi dữ liệu (ETL) cho đến việc đưa vào mô hình AI để gợi ý bài viết cá nhân hóa, đồng thời phải tối ưu chi phí vận hành tiệm cận mức $0.

## Kiến trúc Serverless (Event-Driven)

Hệ thống được thiết kế theo mô hình **Event-Driven Architecture** (Kiến trúc hướng sự kiện) và kiến trúc Zero-ETL với 3 tầng xử lý chính:

1. **Ingestion Layer:** Thu thập dữ liệu clickstream thời gian thực từ giả lập và nén tự động on-the-fly từ JSON sang định dạng cột (Parquet).
2. **Orchestration & ETL Layer:** Điều phối toàn bộ workflow, khắc phục triệt để lỗi "Race Condition" giữa các dịch vụ, và gọi SQL Serverless để biến đổi dữ liệu sang định dạng chuẩn cho AI.
3. **Storage & AI Layer:** Lưu trữ dữ liệu khổng lồ trên Data Lake và huấn luyện mô hình Trí tuệ Nhân tạo (Recommender System) với chiến lược quản trị chi phí khắt khe.

![Sơ đồ kiến trúc hệ thống Clickstream](/aws-project/images/Clickstream/Clicksteam-Diagram.png?featherlight=false&width=90pc)

### Điểm nhấn công nghệ
* **Amazon Kinesis Data Firehose:** Cổng tiếp nhận luồng dữ liệu streaming và ép kiểu trực tiếp JSON sang Parquet dựa vào AWS Glue Schema.
* **AWS Step Functions:** "Nhạc trưởng" điều phối toàn bộ workflow, xử lý hoàn hảo bài toán Data Latency và lỗi Race Condition bằng Wait State.
* **AWS Lambda & Amazon Athena:** Xử lý logic Serverless ETL biến đổi dữ liệu cực nhanh mà không cần duy trì máy chủ.
* **Amazon S3:** Kho lưu trữ vật lý (Data Lake) chứa file Parquet và CSV.
* **Amazon Personalize:** Mô hình học máy tự động (AutoML) gợi ý bài viết kết hợp chiến lược FinOps "Hit and Run" siêu tiết kiệm.

---

## Nội dung

{{% children %}}
