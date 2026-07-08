---
title : "Xác minh kết quả"
date :  "2026-05-13" 
weight : 2
chapter : false
pre : " <b> 3.2. </b> "
---

#### 1. Kiểm tra kho lưu trữ DynamoDB

Ngay khi script Python đang chạy, dữ liệu đã được đẩy qua IoT Core, vào SQS và được Lambda ghi thẳng xuống cơ sở dữ liệu.

1. Quay lại AWS Console, mở **DynamoDB**.
2. Chọn **Explore items** (Khám phá dữ liệu) ở menu bên trái.
3. Chọn bảng `IoT_Fleet_Data` của bạn.
4. Nhấn nút **Run** (Hoặc Scan). Bạn sẽ thấy hàng loạt bản ghi (Items) hiện ra với đầy đủ thông tin: `truck_id`, `temperature`, `latitude`, `longitude` và `timestamp_ms`.

![Dữ liệu DynamoDB](/images/IoTSentinel/3-kiem-tra/dynamo_data.png?featherlight=false&width=90pc)

*Dữ liệu được cập nhật liên tục theo thời gian thực (Real-time)!*

#### 2. Kiểm tra Email cảnh báo khẩn cấp

Trong mã nguồn giả lập, nhiệt độ được thiết lập dao động ngẫu nhiên. Nếu có bất kỳ xe tải nào có nhiệt độ vượt ngưỡng **8.0°C**, hàm Lambda sẽ lập tức kích hoạt SNS.

1. Hãy mở hộp thư Email cá nhân của bạn (Email đã đăng ký ở Bài 2.1).
2. Bạn sẽ thấy các email cảnh báo được gửi đến với tiêu đề: **Cảnh báo nhiệt độ vắc-xin**.
3. Nội dung email sẽ chỉ đích danh xe tải nào đang gặp sự cố và mức nhiệt độ hiện tại là bao nhiêu.

![Email cảnh báo](/images/IoTSentinel/3-kiem-tra/email_alert.png?featherlight=false&width=90pc)

---

