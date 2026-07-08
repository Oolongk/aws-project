---
title : "Khởi tạo DynamoDB & SNS"
date :  "2026-05-13" 
weight : 1
chapter : false
pre : " <b> 1. </b> "
---

#### 1. Khởi tạo kho lưu trữ Amazon DynamoDB

Amazon DynamoDB là cơ sở dữ liệu NoSQL với tốc độ phản hồi tính bằng mili-giây, cực kỳ phù hợp để lưu trữ dữ liệu chuỗi thời gian (time-series) liên tục đổ về từ các xe tải.

1. Truy cập **AWS Management Console**, tìm kiếm và mở **DynamoDB**.
2. Ở menu bên trái, chọn **Tables** và nhấn nút **Create table**.
3. Cấu hình bảng với các thông số sau:
   - **Table name**: `IoT_Fleet_Data`
   - **Partition key**: `truck_id` (Kiểu: **String**) - *Dùng để gom nhóm dữ liệu theo từng xe tải.*
   - **Sort key**: `timestamp_ms` (Kiểu: **Number**) - *Dùng để sắp xếp dữ liệu hành trình theo thời gian thực.*

![Tạo bảng DynamoDB](/images/IoTSentinel/2-trien-khai/dynamodb-create.png?featherlight=false&width=90pc)

4. Ở phần **Table settings**, giữ nguyên lựa chọn **Default settings**.
![Tạo bảng DynamoDB](/images/IoTSentinel/2-trien-khai/dynamodb-create-2.png?featherlight=false&width=90pc)

5. Kéo xuống dưới cùng và nhấn **Create table**. Quá trình tạo sẽ mất khoảng vài giây.

![DynamoDB Success](/images/IoTSentinel/2-trien-khai/dynamodb_success.png?featherlight=false&width=90pc)

---

#### 2. Khởi tạo kênh cảnh báo Amazon SNS

Amazon Simple Notification Service (SNS) sẽ giúp chúng ta gửi thông báo ngay lập tức vào Email của người quản lý khi AWS Lambda phát hiện nhiệt độ của xe tải vượt ngưỡng cho phép.

1. Tìm kiếm và mở dịch vụ **Simple Notification Service (SNS)**.
2. Ở menu bên trái, chọn **Topics** và nhấn **Create topic**.
3. Tại trang tạo Topic, cấu hình như sau:
   - **Type**: Chọn **Standard** *(Lưu ý: Bắt buộc chọn Standard vì loại FIFO không hỗ trợ gửi Email).*
   - **Name**: `TemperatureAlerts`

![Tạo SNS Topic](/images/IoTSentinel/2-trien-khai/sns_topic.png?featherlight=false&width=90pc)

4. Kéo xuống dưới cùng và nhấn **Create topic**.

**Đăng ký Email nhận cảnh báo:**

Sau khi tạo Topic thành công, bạn sẽ được chuyển đến trang chi tiết của Topic đó. Bây giờ, chúng ta cần khai báo Email nhận thông báo.

1. Nhấn vào nút **Create subscription**.
2. Cấu hình Subscription:
   - **Protocol**: Chọn **Email**.
   - **Endpoint**: Nhập địa chỉ Email thật của bạn (Ví dụ: `admin@gmail.com`).

![Tạo Subscription](/images/IoTSentinel/2-trien-khai/sns_sub.png?featherlight=false&width=90pc)

3. Nhấn **Create subscription**. Trạng thái lúc này sẽ là *Pending confirmation*.
4. **Xác thực Email**: Mở hộp thư Email của bạn, tìm email có tiêu đề *AWS Notification - Subscription Confirmation* và nhấn vào liên kết **Confirm subscription**.

![Xác nhận Email](/images/IoTSentinel/2-trien-khai/sns_confirm.png?featherlight=false&width=90pc)
![Xác nhận Email](/images/IoTSentinel/2-trien-khai/sns_confirm_2.png?featherlight=false&width=90pc)
![Xác nhận Email](/images/IoTSentinel/2-trien-khai/sns_confirm_3.png?featherlight=false&width=90pc)
