---
title: "Tầng Phân Tích Dữ Liệu (Analytics Layer)"
date: 2026-06-29
weight: 30
chapter: true
pre: "<b>3. </b>"
---

# Tầng Phân Tích Dữ Liệu (Analytics Layer)

Sau khi dữ liệu đã được làm phẳng và nén thành Parquet ở Chương 2, chúng đã sẵn sàng để khai thác. Tuy nhiên, thay vì phải tải dữ liệu về máy để phân tích, chúng ta sẽ sử dụng **Amazon Athena** – một dịch vụ truy vấn SQL Serverless siêu mạnh mẽ của AWS.

Athena cho phép bạn viết các câu lệnh SQL quen thuộc để truy vấn trực tiếp lên các file trên S3 mà không cần phải thiết lập hay quản lý bất kỳ máy chủ cơ sở dữ liệu nào. Ở chương này, chúng ta sẽ học kỹ thuật **Partition Projection** để tối ưu hóa hiệu suất truy vấn.

{{% children %}}