---
title : "Chạy giả lập xe tải"
date :  "2026-05-13" 
weight : 1
chapter : false
pre : " <b> 3.1. </b> "
---

#### 1. Cập nhật mã nguồn Python

Quay trở lại thư mục dự án trên máy tính của bạn, mở file `truck_simulator.py` (đã tạo ở Chương 1) lên và tiến hành cập nhật 2 thông tin quan trọng nhất mà chúng ta vừa lấy được từ AWS IoT Core ở Bài 2.3:

1. **IOT_ENDPOINT**: Dán địa chỉ Endpoint của bạn vào.
2. **Chứng chỉ bảo mật**: Đảm bảo đường dẫn tới 3 file chứng chỉ (`Root CA`, `Certificate`, `Private Key`) là chính xác.

```python
# ==========================================
# 🔴 CẤU HÌNH THÔNG SỐ 
# ==========================================
IOT_ENDPOINT = "afjy7...-ats.iot.ap-southeast-1.amazonaws.com" # Thay bằng của bạn

PATH_TO_ROOT_CA = "certs/AmazonRootCA1.pem"
PATH_TO_CERT = "certs/128eb8547f...-certificate.pem.crt" # Đổi đúng tên file của bạn
PATH_TO_PRIVATE_KEY = "certs/128eb8547f...-private.pem.key" # Đổi đúng tên file của bạn
```

Lưu file lại.

#### 2. Kích hoạt đội xe tải

Bây giờ, hãy mở **Terminal** (hoặc Command Prompt) tại đúng thư mục chứa file `truck_simulator.py` và chạy lệnh sau:

```bash
python truck_simulator.py
```

Nếu mọi cấu hình chính xác, bạn sẽ thấy Terminal in ra thông báo kết nối thành công và liên tục đẩy dữ liệu GPS cùng nhiệt độ (từ 2°C - 8°C) lên AWS mỗi giây!

![Chạy script Python](/aws-project/images/IoTSentinel/3-kiem-tra/run_script.png?featherlight=false&width=90pc)

> **Mẹo:** Cứ để Terminal chạy như vậy để giả lập xe tải đang đi trên đường. Chúng ta sẽ chuyển sang trình duyệt để xem AWS "hứng" dữ liệu này như thế nào.