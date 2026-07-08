---
title: "Tổng quan Dự án"
date: 2026-05-13
weight: 1
chapter: false
---

## Bài toán đặt ra
Trong ngành vận tải y tế (vắc-xin) hoặc thực phẩm đông lạnh, việc duy trì nhiệt độ ổn định là yếu tố sống còn. Việc giám sát thủ công là không thể với hàng ngàn xe tải đang di chuyển, và chỉ một sự cố hỏng hệ thống làm mát cũng có thể gây thiệt hại khổng lồ.

## Kiến trúc Serverless (Event-Driven)

Hệ thống được thiết kế theo mô hình **Event-Driven Architecture** (Kiến trúc hướng sự kiện) với 3 tầng chính:

1.  **Ingestion Layer:** Thu thập dữ liệu GPS và nhiệt độ thời gian thực từ các thiết bị IoT trên xe tải.
2.  **Processing & Buffering Layer:** Đệm luồng dữ liệu khổng lồ và xử lý logic tự động để phát hiện bất thường.
3.  **Storage & Alerting Layer:** Lưu trữ chuỗi thời gian (time-series) và kích hoạt cảnh báo khẩn cấp.

![Sơ đồ kiến trúc hệ thống](/images/IoT-Sentinel-Diagram.png)

### Điểm nhấn công nghệ
* **AWS IoT Core:** Cổng giao tiếp an toàn nhận dữ liệu MQTT từ hàng ngàn thiết bị.
* **Amazon SQS:** "Giảm xóc" (Buffer) gom dữ liệu, chống quá tải hệ thống.
* **AWS Lambda:** Chạy code Python serverless để xử lý logic không cần quản lý máy chủ.
* **Amazon DynamoDB:** NoSQL Database lưu trữ dữ liệu hành trình siêu tốc độ.
* **Amazon SNS:** Đẩy thông báo khẩn cấp qua Email khi nhiệt độ vượt ngưỡng.