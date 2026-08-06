---
title : "Kiểm tra và Kết quả"
date :  "2026-05-13" 
weight : 3
chapter : false
pre : " <b> 3. </b> "
---

#### Kiểm tra hoạt động của hệ thống

Sau khi đã xây dựng xong toàn bộ hạ tầng Serverless trên AWS ở Chương 2, bây giờ là lúc chúng ta ghép nối tất cả lại với nhau và kích hoạt hệ thống.

Trong chương này, chúng ta sẽ:
1. Cập nhật chứng chỉ bảo mật vào mã nguồn Python và khởi chạy đội xe tải giả lập.
2. Theo dõi dòng dữ liệu thời gian thực chảy vào cơ sở dữ liệu DynamoDB.
3. Kiểm tra hộp thư Email để xác nhận hệ thống cảnh báo tự động hoạt động chính xác khi nhiệt độ vượt ngưỡng an toàn.

Bước kiểm tra này giúp xác minh rằng Data Pipeline của chúng ta (IoT Core ➔ SQS ➔ Lambda ➔ DynamoDB & SNS) đang hoạt động trơn tru.

#### Nội dung

1. [Chạy giả lập xe tải](1-chay-gia-lap/)
2. [Xác minh kết quả](2-xac-minh/)