---
title : "Triển khai hệ thống"
date :  "2026-05-13" 
weight : 2
chapter : false
pre : " <b> 2. </b> "
---

#### Triển khai hệ thống trên AWS

Trong chương này, chúng ta sẽ bắt tay vào cấu hình các dịch vụ Serverless trên **AWS Management Console**. Chiến lược triển khai của chúng ta là đi ngược từ cuối luồng dữ liệu lên đầu:

1. **Storage & Alerting (DynamoDB, SNS)**: Chuẩn bị "kho chứa" dữ liệu hành trình và thiết lập "loa phát thanh" gửi email khi có sự cố.
2. **Processing & Buffering (Lambda, SQS)**: Tạo hàng đợi để hứng dữ liệu tốc độ cao, đồng thời viết hàm xử lý logic kiểm tra nhiệt độ.
3. **Ingestion (IoT Core)**: Tạo thiết bị ảo (Thing), cấp phát chứng chỉ bảo mật và cấu hình luật (Rule) để dẫn luồng dữ liệu vào hàng đợi.

Việc triển khai theo thứ tự này giúp các dịch vụ dễ dàng nhận diện và cấp quyền cho nhau mà không gặp lỗi "không tìm thấy tài nguyên".

#### Nội dung

1. [Khởi tạo DynamoDB & SNS](1-dynamodb-sns/)
2. [Cấu hình SQS & Lambda](2-sqs-lambda/)
3. [Thiết lập IoT Core](3-iot-core/)