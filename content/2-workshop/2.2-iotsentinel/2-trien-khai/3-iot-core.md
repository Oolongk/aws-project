---
title : "Thiết lập AWS IoT Core"
date :  "2026-05-13" 
weight : 3
chapter : false
pre : " <b> 3. </b> "
---

#### 1. Tạo "Thing" cho xe tải
Trong AWS IoT Core, mỗi xe tải được coi là một "Thing". Chúng ta sẽ tạo một định danh đại diện cho đội xe.

1. Mở dịch vụ **IoT Core**.
2. Vào **Manage** > **All devices** > **Things** > Nhấn **Create things**.
3. Chọn **Create single thing** > Nhấn **Next**.
4. **Thing name**: `Vaccine_Truck_Fleet` > Nhấn **Next**.
5. Chọn **Auto-generate a new certificate** > Nhấn **Next**.

**Tải Chứng chỉ bảo mật (Cực kỳ quan trọng):**
1. Tại trang **Download certificates**, bạn hãy tải xuống 3 file sau:
   - `Device certificate`
   - `Private key file`
   - `Amazon Root CA 1`
2. **Lưu ý**: Sau khi rời trang này bạn sẽ không bao giờ tải lại được Private key. Hãy lưu chúng vào thư mục `certs/` trong dự án của bạn trên máy tính.

![Tải chứng chỉ IoT](/aws-project/images/IoTSentinel/2-trien-khai/iot_certs.png?featherlight=false&width=90pc)

3. Nhấn **Done**. (Tạm thời bỏ qua phần Attach Policy, chúng ta sẽ dùng Policy mặc định).

---

#### 2. Cấu hình IoT Rule (Định tuyến dữ liệu)
Luật (Rule) này sẽ tự động bắt các bản tin gửi lên Topic `telemetry/trucks` và đẩy thẳng vào hàng đợi SQS đã tạo ở bài 2.2.

1. Vào menu **Message routing** > **Rules** > Nhấn **Create rule**.
![Cấu hình IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_1.png?featherlight=false&width=90pc)

2. **Rule name**: `IoT_To_SQS_Rule`.
![Cấu hình IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_2.png?featherlight=false&width=90pc)

3. **SQL statement**: Nhập câu lệnh để lấy toàn bộ dữ liệu:
   ```sql
   SELECT * FROM 'telemetry/trucks'
   ```
4. Nhấn **Next**.
![Cấu hình IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_3.png?featherlight=false&width=90pc)

5. **Attach action**: Chọn **SQS queue**.
   - Chọn hàng đợi: `IoT_Fleet_Queue`.
6. Nhấn **Create**.

![Cấu hình IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_4.png?featherlight=false&width=90pc)

---

#### 3. Lấy Endpoint kết nối

Để phần mềm giả lập xe tải biết "nhà" của AWS ở đâu để gửi dữ liệu tới, bạn cần lấy địa chỉ **Endpoint** duy nhất của tài khoản. Ở giao diện mới, thông tin này đã được chuyển vào mục Cấu hình miền.

1. Tại thanh menu bên trái của **AWS IoT Core**, bạn cuộn lên phần trên cùng.
2. Tìm nhóm menu **Connect** (Kết nối) và chọn **Domain configurations** (Cấu hình miền).
3. Tại giao diện chính, bạn sẽ thấy cột **Domain name**. Đây chính là địa chỉ Endpoint của bạn.
4. Hãy copy chuỗi địa chỉ này (có dạng `afjy7...-ats.iot.ap-southeast-1.amazonaws.com`) và lưu lại để sử dụng cho Chương 3.

![Lấy IoT Endpoint từ Domain Configuration](/aws-project/images/IoTSentinel/2-trien-khai/iot_endpoint_new.png?featherlight=false&width=90pc)


