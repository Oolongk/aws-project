---
title: "Chuẩn bị Tài nguyên (Preparation)"
date: 2026-06-25
weight: 1
chapter: true
pre: "Chương 1. "
---
# Chuẩn bị Tài nguyên (Preparation)
Trước khi bắt tay vào xây dựng đường ống dữ liệu (Data Pipeline), chúng ta cần chuẩn bị sẵn sàng các "nguyên liệu" nền tảng trên đám mây AWS. 

Chương này sẽ hướng dẫn bạn khởi tạo 3 thành phần cốt lõi:
1. **Kho lưu trữ vật lý (Amazon S3):** Nơi chứa dữ liệu Data Lake.
2. **Khuôn mẫu dữ liệu (AWS Glue Schema):** Định nghĩa cấu trúc để nén JSON sang Parquet.
3. **Kênh thông báo (Amazon SNS):** Thiết lập hệ thống tự động gửi Email báo cáo.

Việc chuẩn bị tốt các tài nguyên này sẽ giúp các bước lắp ráp kiến trúc ở những chương sau diễn ra mượt mà và không gặp lỗi phụ thuộc (Dependencies error).
#### Nội dung
{{% children %}}