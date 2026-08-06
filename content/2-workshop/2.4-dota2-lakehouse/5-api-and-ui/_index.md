---
title: "Tầng API & Giao Diện Người Dùng (API & UI Layer)"
date: 2026-06-29
weight: 50
chapter: true
pre: "<b>5. </b>"
---

# Tầng API & Giao Diện Người Dùng (API & UI Layer)

Khi dữ liệu tổng hợp (Metrics) đã được nạp an toàn vào Amazon DynamoDB ở Chương 4, khâu cuối cùng là xây dựng một cổng giao tiếp API và giao diện để người dùng có thể tra cứu.

Trong chương này, chúng ta sẽ thiết lập một kiến trúc API Serverless hoàn chỉnh: sử dụng **AWS Lambda** làm Backend bóc tách dữ liệu từ DynamoDB, đứng sau cổng kiểm soát **Amazon API Gateway** để tiếp nhận các yêu cầu HTTP request từ phía **Website Frontend** lưu trữ trên S3.

{{% children %}}