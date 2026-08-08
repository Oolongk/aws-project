---
weight: 2
date: 2026-06-29
title: "Tầng Xử Lý Dữ Liệu (Processing Layer)"
chapter: false
pre: "<b>2.4.2. </b>"
---

Sau khi dữ liệu thô (JSON) đã hạ cánh xuống S3 Raw Bucket, chúng ta cần một cỗ máy mạnh mẽ để làm sạch, làm phẳng (Flatten) và chuyển đổi định dạng dữ liệu nhằm tối ưu chi phí lưu trữ.

Trong chương này, chúng ta sẽ sử dụng **AWS Glue** (chạy nền tảng Apache Spark) để thực hiện công việc nặng nhọc này và ghi kết quả ra định dạng cột **Parquet**.

{{% children %}}