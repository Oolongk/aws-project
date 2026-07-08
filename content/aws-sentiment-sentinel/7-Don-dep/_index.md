---
title: "7. Dọn dẹp tài nguyên (Clean up)"
date: 2026-03-18
weight: 7
---

Chúc mừng bạn đã hoàn thành dự án! Trong thế giới Điện toán Đám mây (Cloud Computing), tài nguyên sinh ra tiền, nhưng nếu để quên thì nó sẽ "đốt" tiền. Dù dự án của chúng ta sử dụng chủ yếu các dịch vụ Serverless nằm trong gói Free Tier, việc dọn dẹp (Clean up) sạch sẽ sau khi thực hành vẫn là một thói quen bắt buộc của mọi Kỹ sư Dữ liệu chuyên nghiệp.

Dưới đây là thứ tự dọn dẹp chuẩn xác để bạn không bỏ sót bất kỳ "tài nguyên Zombie" nào.

---

### Bước 1: Hủy đăng ký AWS QuickSight (Ưu tiên số 1)
QuickSight là dịch vụ tính phí theo tháng ($24/tháng), do đó đây là thứ bạn phải "tiêu diệt" đầu tiên.

1. Đăng nhập vào **AWS QuickSight**.
2. Bấm vào biểu tượng Avatar ở góc trên cùng bên phải -> Chọn **Manage QuickSight**.
3. Chọn **Account settings** ở menu bên trái.
4. Kéo xuống dưới cùng và bấm **Delete account** (hoặc Unsubscribe).
5. Làm theo hướng dẫn trên màn hình (thường yêu cầu gõ lại tên account) để xác nhận xóa. 
*(Lưu ý: Thao tác này sẽ xóa vĩnh viễn mọi Dashboard và Dataset của bạn).*

---

### Bước 2: Tắt đồng hồ báo thức Amazon EventBridge
Nếu không tắt cái này, sáng mai hệ thống lại tự động thức dậy cào dữ liệu và sinh ra chi phí mới.

1. Truy cập dịch vụ **Amazon EventBridge** -> Chọn **Schedules** ở menu bên trái.
2. Tìm lịch trình `Daily-Youtube-Data-Ingestion` mà bạn đã tạo ở Chương 6.
3. Tích chọn nó và bấm **Delete**.

---

### Bước 3: Dọn dẹp kho lưu trữ Amazon S3 (Rất quan trọng)
AWS không cho phép bạn xóa một Bucket nếu bên trong nó vẫn còn chứa file. Bạn phải "đổ rác" trước khi đập thùng.

1. Truy cập **Amazon S3** -> Chọn **Buckets**.
2. Tìm Bucket Data Lake của bạn (và cả Bucket chứa kết quả Athena `athena_results` nếu có).
3. **Đổ rác:** Tích chọn Bucket -> Bấm nút **Empty** ở menu phía trên -> Gõ chữ `permanently delete` để xác nhận dọn sạch file bên trong.
4. **Xóa thùng:** Sau khi Empty thành công, tích chọn lại Bucket đó -> Bấm **Delete** -> Nhập tên Bucket để xác nhận xóa vĩnh viễn.

---

### Bước 4: Xóa Database, Hàng đợi và Hàm xử lý

Lần lượt truy cập vào các dịch vụ sau và nhấn Delete:

1. **Amazon DynamoDB:**
   - Vào mục **Tables**. Tích chọn bảng `YoutubeCommentsTracker` -> Bấm **Delete**.
   - Làm tương tự với bảng `YoutubeVideoBlacklist`.
2. **Amazon SQS:**
   - Vào mục **Queues**. Tích chọn `YoutubeVideoQueue` -> Bấm **Delete**.
3. **AWS Lambda:**
   - Vào mục **Functions**. Tích chọn cả 3 hàm: `Producer_Lambda`, `Consumer_Lambda`, `Transformer_Lambda`.
   - Bấm **Actions** -> Chọn **Delete**.
4. **Amazon Athena (Tùy chọn):**
   - Dữ liệu gốc trên S3 đã bị xóa nên các bảng trong Athena cũng sẽ tự động mất tác dụng. Bạn có thể mở Query Editor và chạy lệnh `DROP DATABASE sentiment_db CASCADE;` để dọn dẹp nốt lược đồ ảo.

---

### Bước 5: Dọn dẹp IAM Roles (Tùy chọn nâng cao)
Dù IAM không tính phí, nhưng việc xóa các Role không dùng đến giúp tài khoản của bạn gọn gàng và bảo mật hơn.

1. Truy cập **AWS IAM** -> Chọn **Roles**.
2. Tìm và xóa các Role bạn đã tạo cho Lambda (ví dụ: Role có quyền truy cập SQS, DynamoDB, Bedrock).

---