---
title : "Dọn dẹp tài nguyên"
date :  "2026-05-13" 
weight : 4
chapter : true
pre : " <b> 4. </b> "
---

#### Dọn dẹp tài nguyên

#### 1. Xóa cấu hình AWS IoT Core
1. Truy cập **IoT Core** > **Manage** > **All devices** > **Things**.
2. Chọn `Vaccine_Truck_Fleet` và nhấn **Delete**.
3. Vào **Message routing** > **Rules**, chọn `IoT_To_SQS_Rule` và nhấn **Delete**.

![Xóa tài nguyên IoT](/aws-project/images/IoTSentinel/4-don-dep/IoT-1.png?featherlight=false&width=90pc)
![Xóa tài nguyên IoT](/aws-project/images/IoTSentinel/4-don-dep/IoT-2.png?featherlight=false&width=90pc)
![Xóa tài nguyên IoT](/aws-project/images/IoTSentinel/4-don-dep/IoT-3.png?featherlight=false&width=90pc)

#### 2. Xóa bộ xử lý Lambda & Hàng đợi SQS
1. Mở dịch vụ **Lambda** > **Functions**, chọn `IoT_Process_Data` và nhấn **Delete**.

![Xóa Lambda và SQS](/aws-project/images/IoTSentinel/4-don-dep/Lambda-1.png?featherlight=false&width=90pc)
![Xóa Lambda và SQS](/aws-project/images/IoTSentinel/4-don-dep/Lambda-2.png?featherlight=false&width=90pc)

2. Mở dịch vụ **SQS** > **Queues**, chọn `IoT_Fleet_Queue` và nhấn **Delete**. Nhập chữ `confirm` vào ô xác nhận.

![Xóa Lambda và SQS](/aws-project/images/IoTSentinel/4-don-dep/SQS-1.png?featherlight=false&width=90pc)

#### 3. Xóa Database DynamoDB & Thông báo SNS
1. Mở dịch vụ **DynamoDB** > **Tables**, chọn bảng `IoT_Fleet_Data` và nhấn **Delete**. Nhập `confirm` để xác nhận.

![Xóa DynamoDB và SNS](/aws-project/images/IoTSentinel/4-don-dep/Dynamodb-1.png?featherlight=false&width=90pc)
![Xóa DynamoDB và SNS](/aws-project/images/IoTSentinel/4-don-dep/Dynamodb-2.png?featherlight=false&width=90pc)


2. Mở dịch vụ **SNS** > **Topics**, chọn `TemperatureAlerts` và nhấn **Delete**.

![Xóa DynamoDB và SNS](/aws-project/images/IoTSentinel/4-don-dep/SNS-1.png?featherlight=false&width=90pc)
![Xóa DynamoDB và SNS](/aws-project/images/IoTSentinel/4-don-dep/SNS-2.png?featherlight=false&width=90pc)

---

#### Tổng kết dự án

Thông qua bài Lab này, bạn đã nắm vững cách xây dựng một luồng **Data Pipeline** hoàn chỉnh:
- **Thiết lập thiết bị Edge**: Dùng Python giả lập dữ liệu hành trình xe tải.
- **Thu thập dữ liệu**: Sử dụng IoT Core và giao thức MQTT.
- **Điều tiết & Xử lý**: Dùng SQS để đệm dữ liệu và Lambda để xử lý logic thời gian thực.
- **Lưu trữ & Cảnh báo**: Dùng DynamoDB lưu trữ bền vững và SNS gửi thông báo khẩn cấp qua Email.