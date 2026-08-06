---
title: "6. Tự động hóa toàn phần (Full Automation) với Amazon EventBridge"
date: 2026-03-14
weight: 6
---

Một hệ thống dữ liệu Serverless chỉ thực sự hoàn thiện khi nó đạt trạng thái "Zero-touch" – tự động vận hành mà không cần con người can thiệp. Ở chương cuối cùng này, chúng ta sẽ thiết lập đồng hồ sinh học cho toàn bộ dự án: Tự động thức dậy cào dữ liệu vào 8:00 sáng mỗi ngày, và tự động cập nhật báo cáo lên Dashboard để sếp có thể xem cùng ly cà phê sáng.

### Mục tiêu của chặng này:
1. Cấu hình Amazon EventBridge Scheduler để kích hoạt `Producer_Lambda` mỗi ngày.
2. Lên lịch làm mới (Refresh) bộ nhớ SPICE trên AWS QuickSight.

---

### Bước 1: Lên lịch chạy Pipeline với Amazon EventBridge

EventBridge Scheduler là công cụ lập lịch hiện đại của AWS, cho phép chúng ta kích hoạt các dịch vụ theo múi giờ địa phương một cách chính xác.

1. Truy cập dịch vụ **Amazon EventBridge** trên AWS Console.
2. Tại menu bên trái, tìm mục *Scheduler* và chọn **Schedules** -> Bấm **Create schedule**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-1.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-2.png)
   
3. **Bước 1: Specify schedule detail (Chi tiết lịch trình)**
   - **Schedule name:** `Daily-Youtube-Data-Ingestion`
   - **Schedule pattern:** Chọn *Recurring schedule* (Lặp lại).
   - **Schedule type:** Chọn *Cron-based schedule*.
   - **Cron expression:** Điền `0 8 * * ? *` (Tương đương 8:00 AM mỗi ngày).
   - **Timezone:** Gõ và chọn múi giờ của bạn, ví dụ: `Asia/Ho_Chi_Minh`.
   - Bấm **Next**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-3.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-4.png)
  
4. **Bước 2: Select target (Chọn mục tiêu)**
   - Chọn **AWS Lambda**.
   - Tại mục *Lambda function*, trỏ vào hàm **`Producer_Lambda`** của bạn.
   - Bấm **Next**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-5.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-6.png)
  
5. **Bước 3: Settings**
   - Giữ nguyên các thông số mặc định. Hệ thống sẽ tự động tạo một IAM Role mới cho phép EventBridge gọi hàm Lambda này.
   - Bấm **Next**, sau đó kiểm tra lại tổng thể và bấm **Create schedule**.

Từ lúc này, cứ đúng 8:00 sáng (giờ VN), EventBridge sẽ khởi động hàm Producer. Kéo theo đó, SQS, Consumer, S3, và Transformer Lambda sẽ tự động chạy theo phản ứng dây chuyền (Chain reaction) mà chúng ta đã thiết lập ở các chương trước. Toàn bộ quá trình cào và phân tích AI thường mất khoảng 10-15 phút.

---

### Bước 2: Tự động làm mới Dataset trên AWS QuickSight

Dữ liệu mới đã nằm trong S3, nhưng bộ nhớ đệm SPICE của QuickSight cần được "nhắc nhở" để kéo dữ liệu mới này lên Dashboard. Vì Pipeline chạy lúc 8:00 AM và mất khoảng 15 phút để hoàn tất, chúng ta sẽ đặt lịch cho QuickSight cập nhật vào lúc **8:30 AM** (để dư dả thời gian an toàn).

1. Mở giao diện **AWS QuickSight**.
2. Tại menu bên trái, chọn **Datasets**.
3. Bấm vào Datasets của dự án.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-1.png)
   
4. Chuyển sang tab **Refresh** -> Bấm **Add schedule**.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-2.png)
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-3-0.png)

   
5. Cấu hình lịch cập nhật (Refresh setup):
   - **Frequency:** Daily (Hàng ngày).
   - **Timezone:** `Asia/Ho_Chi_Minh`.
   - **Start time:** `08:30`.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-3.png)
  
1. Bấm **Save**.

---

### Tổng kết Series

Chúc mừng bạn đã hoàn thành trọn vẹn dự án **AWS Sentiment Sentinel**! 

Từ một danh sách từ khóa đơn giản, chúng ta đã xây dựng thành công một Data Pipeline cấp độ Production hội tụ đủ các công nghệ tối tân nhất:
- **Tách rời dịch vụ (Decoupling):** Amazon SQS.
- **Tính toán phi máy chủ (Serverless Compute):** AWS Lambda.
- **Hồ dữ liệu (Data Lake):** Amazon S3 & DynamoDB.
- **Trí tuệ nhân tạo (Generative AI):** Amazon Bedrock (Claude 3.5 Haiku).
- **Phân tích dữ liệu (Data Analytics):** Amazon Athena & QuickSight.
- **Tự động hóa (Automation):** Amazon EventBridge.

Dự án này không chỉ chứng minh khả năng lập trình Python, mà còn thể hiện tư duy kiến trúc hệ thống (System Architecture), khả năng kiểm soát chi phí (Cost-optimization), và kỹ năng xử lý ngoại lệ (Error Handling) của một Data Engineer chuyên nghiệp. Hệ thống hiện tại có thể chạy ẩn danh mượt mà hàng tháng trời với chi phí gần như bằng $0 (trong khuôn khổ AWS Free Tier).