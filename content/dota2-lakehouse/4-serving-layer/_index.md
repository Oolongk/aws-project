---
title: "Tầng Phục Vụ Dữ Liệu (Serving Layer)"
date: 2026-06-29
weight: 40
chapter: true
pre: "<b>4. </b>"
---

# Tầng Phục Vụ Dữ Liệu (Serving Layer)

Dữ liệu phân tích dù có hay đến mấy cũng sẽ trở nên vô giá trị nếu hệ thống mất tới vài phút để hiển thị nó lên màn hình cho người dùng. 

Trong chương này, chúng ta sẽ xây dựng **Speed Layer** cho hệ thống bằng cách sử dụng cơ sở dữ liệu NoSQL **Amazon DynamoDB**. Bộ máy AWS Glue PySpark sau khi xử lý dữ liệu sạch sẽ trực tiếp tính toán sẵn các chỉ số Meta (Aggregated Metrics) và nạp thẳng vào DynamoDB, đảm bảo ứng dụng Frontend có thể truy xuất thông tin với độ trễ dưới 100ms.

{{% children %}}