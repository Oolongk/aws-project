---
title: "5. Trực quan hóa dữ liệu: Amazon Athena và AWS QuickSight"
date: 2026-03-14
weight: 5
---

Bước cuối cùng của kiến trúc Data Pipeline là lớp Trình bày (Presentation Layer). Thay vì phải xây dựng các luồng ETL (Extract, Transform, Load) phức tạp để đưa dữ liệu vào một Database truyền thống, hệ thống sẽ sử dụng **Amazon Athena** để truy vấn trực tiếp các file JSON trên S3 bằng SQL (kiến trúc Schema-on-read). Sau đó, dữ liệu được đẩy vào bộ nhớ SPICE của **Amazon QuickSight** để xây dựng BI Dashboard.

### Mục tiêu của chặng này:
1. Định nghĩa lược đồ dữ liệu bằng Amazon Athena (UI Query Editor v3).
2. Cấu hình phân quyền IAM Security thống nhất cho QuickSight.
3. Xây dựng Dashboard giám sát cảm xúc người dùng.

---

### Bước 1: Khởi tạo lược đồ với Amazon Athena

Amazon Athena cho phép đọc trực tiếp dữ liệu thô trên S3 mà không cần vận hành máy chủ (Serverless SQL).

1. Truy cập dịch vụ **Amazon Athena** trên AWS Console.
2. **Cấu hình Output Location (Bắt buộc):**
   - Từ menu bên trái, chọn **Query editor**
   - Tại màn hình Editor v3, nhìn sang góc phải chọn tab **Query Settings** -> Bấm **Manage**.
   - Tại mục *Query result location*, chỉ định một đường dẫn S3 dùng để lưu log truy vấn (Folder athena_result đã tạo ở mục 2). Bấm **Save**.
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-0.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-1.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-2.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-3.png)

1. Quay lại tab **Editor**, chạy lệnh DDL sau để tạo cơ sở dữ liệu:
   ```sql
   CREATE DATABASE IF NOT EXISTS sentiment_db;
   ```
2. Chọn cơ sở dữ liệu `sentiment_db` vừa tạo ở thanh *Database* bên trái.
3. Chạy lệnh SQL sau để định nghĩa bảng, ánh xạ trực tiếp vào thư mục dữ liệu đã qua xử lý trên S3:
   ```sql
   CREATE EXTERNAL TABLE IF NOT EXISTS youtube_comments (
     `id` string,
     `language` string,
     `vietnamese_text` string,
     `sentiment` string
   )
   ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
   LOCATION 's3://<bucket-cua-ban>/processed_data/';
   ```
   *(Lưu ý: Thay `<bucket-cua-ban>` bằng tên Bucket Data Lake thực tế của dự án).*
4. Truy vấn thử nghiệm để xác nhận dữ liệu đã được nạp thành công:
   ```sql
   SELECT * FROM youtube_comments LIMIT 10;
   ```

---

### Bước 2: Xây dựng View chuẩn hóa

Thay vì phơi bày bảng gốc (`youtube_comments_raw`) cho QuickSight, chúng ta sẽ tạo một **View**. Lớp này giúp đổi tên cột cho thân thiện với Business User và lọc bỏ các bản ghi bị lỗi (nếu có) để tiết kiệm dung lượng SPICE.

Tại tab Editor của Athena, chạy lệnh SQL sau:

```sql
CREATE OR REPLACE VIEW vw_youtube_sentiment AS
SELECT 
    id AS comment_id,
    UPPER(language) AS source_language,
    vietnamese_text AS translated_summary,
    UPPER(sentiment) AS sentiment_label
FROM youtube_comments_raw
WHERE sentiment IS NOT NULL 
  AND sentiment != 'UNKNOWN'
  AND sentiment != 'KHÔNG XÁC ĐỊNH';
```
Bây giờ, QuickSight sẽ chỉ làm việc với View sạch sẽ `vw_youtube_sentiment` này.

---

### Bước 3: Cấp quyền truy cập S3 cho QuickSight

Đây là bước cấu hình bảo mật quan trọng. Giao diện Security 2026 của QuickSight yêu cầu người quản trị phải cấp quyền Write rõ ràng cho Athena Workgroup để tránh lỗi `AccessDenied` khi load biểu đồ.

1. Truy cập dịch vụ **QuickSight**. *(Thực hiện đăng ký tài khoản Standard/Enterprise nếu đây là lần truy cập đầu tiên).*
2. Tại giao diện chính, bấm vào biểu tượng Avatar (góc trên cùng bên phải) -> Chọn **Manage QuickSight**.
3. Ở menu điều hướng bên trái, chọn **AWS Resources**.
5. Cấu hình quyền truy cập (IAM Policies):
   - Tích chọn **Amazon Athena**. Nhấn *Next* trên popup hiển thị.
   - Tích chọn **Amazon S3**. Một bảng danh sách các Bucket sẽ hiện lên.
   - **BƯỚC QUAN TRỌNG:** Tìm và tích vào Bucket Data Lake của bạn để cấp quyền Đọc (Read). Bắt buộc phải tích thêm vào ô **Write permission for Athena Workgroup** ở cột kế bên để QuickSight có quyền ghi log kết quả truy vấn.
6. Bấm **Save**.
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-1.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-2.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-3.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-4.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-5.png)

---

### Bước 4: Nạp dữ liệu vào SPICE Engine

SPICE (Super-fast, Parallel, In-memory Calculation Engine) là bộ nhớ đệm của QuickSight. Việc đưa dữ liệu vào SPICE giúp tăng tốc độ phản hồi của biểu đồ và giảm chi phí quét dữ liệu trực tiếp trên S3 thông qua Athena.

1. Quay lại trang chủ QuickSight, chọn tab **Datasets** (menu trái) -> Bấm **New dataset**.
2. Chọn Data Source: **Athena**.
3. Điền tên nguồn dữ liệu: `YoutubeSentiment_Source` -> Bấm **Create data source**.
4. Tại bảng chọn cấu trúc (Schema):
   - **Catalog:** `AwsDataCatalog`
   - **Database:** `sentiment_db`
   - **Table:** `youtube_comments`
   - Bấm **Select**.
5. Chọn tuỳ chọn **Import to SPICE for quicker analytics** -> Bấm **Visualize**.

---

### Bước 5: Xây dựng BI Dashboard

Tại màn hình Analysis, thiết lập các biểu đồ (Visuals) cốt lõi để theo dõi chất lượng dữ liệu:

1. **Tổng quan Phân bổ Cảm xúc (Pie Chart):**
   - *Mục đích:* Thể hiện tỷ lệ % các luồng ý kiến (Tích cực, Tiêu cực, Trung lập).
   - *Cấu hình:* Kéo trường `sentiment` vào mục **Group/Color**. Kéo trường `comment_id` vào mục **Value** (mặc định áp dụng hàm Count).
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-1.png)
  
2. **Bảng Đối soát Dữ liệu (Table):**
   - *Mục đích:* Liệt kê chi tiết văn bản để kiểm chứng độ chính xác của mô hình Claude 3.5.
   - *Cấu hình:* Kéo thả các cột `vietnamese_text`, `sentiment`,`author`,`published_at`,`original_text`,`language` vào mục **Group by**.
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-3.png)

3. **Phân loại theo Ngôn ngữ (Donut Chart):**
   - *Mục đích:* Giám sát mức độ đa dạng ngôn ngữ của tập dữ liệu thô cào được từ YouTube.
   - *Cấu hình:* Kéo `language` vào **Group/Color**, `video_id` vào **Value**.
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-4.png)

---

### Tổng kết Dự án

Đến đây, toàn bộ vòng đời của hệ thống Serverless Data Pipeline đã hoàn thiện. Hạ tầng được xây dựng tuân thủ chặt chẽ các nguyên tắc kỹ thuật dữ liệu hiện đại:
- **Tách rời dịch vụ (Decoupled Architecture):** Sử dụng SQS để cô lập rủi ro giữa lớp thu thập và lớp xử lý.
- **Tối ưu chi phí (Cost Optimization):** Áp dụng Chunking và Prompt Engineering để giảm thiểu token LLM; sử dụng SPICE và Schema-on-read thay cho Data Warehouse đắt đỏ.
- **Khả năng mở rộng (Scalability):** Lambda, S3 và Athena tự động co giãn theo dung lượng file JSON đầu vào mà không cần can thiệp hạ tầng.

Hệ thống sẵn sàng vận hành tự động (Production-ready) để xử lý hàng ngàn bình luận mỗi ngày với chi phí gần như bằng không trong khuôn khổ AWS Free Tier.