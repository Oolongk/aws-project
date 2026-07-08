---
title: "Tầng Tiếp nhận (Ingestion Layer)"
date: 2026-06-25
weight: 2
chapter: true
pre: "Chương 2. "
---
# Tầng Tiếp nhận (Ingestion Layer)
Sau khi đã chuẩn bị xong cơ sở hạ tầng, chúng ta bước vào cấu hình tầng tiếp nhận. 

Nhiệm vụ của tầng này là hứng dữ liệu thô dạng JSON từ thiết bị của người dùng, tận dụng AWS Glue Schema đã tạo ở Chương 1 để nén dữ liệu on-the-fly (ngay trên luồng chạy) thành Parquet, và lưu trữ an toàn xuống Amazon S3 Data Lake.
#### Nội dung
{{% children %}}