---
title : "Các bước chuẩn bị"
date :  "2026-05-13" 
weight : 1
chapter : false
pre : " <b> 1. </b> "
---

#### Các bước chuẩn bị

Để xây dựng hệ thống giám sát xe tải thời gian thực, chúng ta cần chuẩn bị một "nguồn phát dữ liệu" giả lập và thiết lập môi trường lập trình trên máy tính cá nhân. Do không có thiết bị phần cứng thật, chúng ta sẽ dùng Python để mô phỏng 10 chiếc xe tải thông minh.

- **Python & AWSIoTPythonSDK**: Đây là bộ công cụ chính để biến máy tính của bạn thành một thiết bị IoT Edge. Thư viện này giúp kết nối bảo mật qua giao thức MQTT với AWS Cloud, mã hóa dữ liệu và gửi thông tin nhiệt độ lên hệ thống.

- **AWS Region (Singapore - ap-southeast-1)**: Để tối ưu tốc độ và chi phí, chúng ta sẽ thống nhất triển khai toàn bộ tài nguyên tại vùng Singapore. Việc chọn đúng Region ngay từ đầu giúp các dịch vụ như SQS, Lambda và DynamoDB có thể liên kết với nhau một cách tự động và an toàn.

Việc chuẩn bị kỹ lưỡng môi trường giả lập là bước đệm quan trọng để dòng dữ liệu có thể chảy suôn sẻ vào Pipeline ở các bước tiếp theo.

#### Nội dung

1. [Thiết lập môi trường Python](1.1-setup-python/)
2. [Mã nguồn Truck Simulator](1.2-ma-nguon/)