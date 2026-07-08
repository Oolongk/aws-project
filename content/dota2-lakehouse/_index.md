---
title: "Xây Dựng Data Lakehouse Serverless: Dota 2 Meta Analytics"
date: 2026-06-29
weight: 1
chapter: true
pre: "<b>"
---

#  Giới thiệu Dự án: Dota 2 Meta Analytics Data Lakehouse

Dota 2 không chỉ là một tựa game eSports tỷ đô với những giải đấu danh giá nhất hành tinh (The International), mà đằng sau nó còn là một **mỏ vàng dữ liệu khổng lồ (Big Data)**. Mỗi giây trôi qua, hàng triệu quyết định di chuyển, sử dụng kỹ năng, và mua trang bị của các game thủ chuyên nghiệp được hệ thống ghi nhận. 

**Bài toán đặt ra:** *Làm thế nào để thu thập hàng trăm ngàn file JSON phức tạp từ API, làm sạch chúng, và phân tích ra được "Meta" (những vị Tướng hay Trang bị nào đang có tỷ lệ thắng cao nhất) để phục vụ cho người chơi tra cứu theo thời gian thực... mà không làm "cháy túi" vì tiền duy trì Server?*

Dự án này chính là câu trả lời. Tôi sẽ hướng dẫn bạn tự tay xây dựng một **Data Lakehouse Serverless 100%** trên AWS. Bằng việc áp dụng triệt để tư duy **FinOps (Tối ưu hóa chi phí đám mây)** và **Decoupling (Phân tách kiến trúc)**, hệ thống này có thể xử lý lượng dữ liệu khổng lồ với chi phí tiệm cận... 0 đồng!

---

## Kiến trúc Hệ thống (Architecture Design)

Dự án được thiết kế theo chuẩn Enterprise Architecture, phân tách rõ ràng thành 4 lớp (Swimlanes) độc lập. Việc phân tách này đảm bảo nếu một lớp bị lỗi (ví dụ API sập), các lớp khác vẫn hoạt động bình thường (Fault Tolerance).

![Dota 2 Serverless Data Pipeline](/images/dota2/Dota2-Pipeline.png?featherlight=false&width=90pc)

### Chi tiết luồng dữ liệu (Data Flow):

**1. Tầng Thu thập (Ingestion & Automation Layer)**
* **Hành động:** Sử dụng **AWS Lambda** (kích hoạt tự động hàng ngày bằng **EventBridge Cron**) để gọi OpenDota API.
* **Kết quả:** Kéo dữ liệu trận đấu chuyên nghiệp về dưới định dạng `JSON` và lưu thẳng vào **Amazon S3 (Raw Zone)**. Dữ liệu được gom nhóm (Partition) theo chuẩn `dt=YYYY-MM-DD` ngay từ đầu.

**2. Tầng Xử lý (Processing / ETL Layer)**
* **Hành động:** Việc có file mới thả vào S3 sẽ giật chuông báo động (S3 Event Notification), tự động đánh thức **AWS Glue (PySpark)** dậy làm việc.
* **Kết quả:** Glue Job sẽ đọc JSON, làm phẳng (Flatten) mảng dữ liệu 10 người chơi phức tạp thành dạng bảng, sau đó ghi ra **Amazon S3 (Processed Zone)** dưới định dạng `Parquet` siêu nén bằng thuật toán Snappy.

**3. Tầng Phân tích (Analytics Layer)**
* **Hành động:** Thiết lập **Amazon Athena** để đội ngũ Data Engineer có thể gõ SQL truy vấn Ad-hoc trực tiếp lên S3 Processed.
* **Tối ưu:** Áp dụng kỹ thuật **Partition Projection** cho Athena thay vì dùng Glue Crawler, giúp tăng tốc truy vấn lên hàng chục lần và giảm thiểu chi phí quét dữ liệu xuống mức thấp nhất.

**4. Tầng Phục vụ (Serving & API Layer)**
* **Hành động:** AWS Glue (từ lớp Processing) sau khi xử lý xong sẽ tính toán sẵn các chỉ số Aggregation (Winrate, Pickrate) và Upsert thẳng vào cơ sở dữ liệu siêu tốc **Amazon DynamoDB**.
* **Phục vụ UI:** Khi người dùng truy cập trang Web tĩnh (lưu trữ trên S3 Static Hosting), Web sẽ gọi HTTP API Gateway $\rightarrow$ Lambda Backend $\rightarrow$ Đọc DynamoDB và trả về kết quả (độ trễ dưới 100ms).
* **Tuyệt chiêu FinOps:** Các dữ liệu tĩnh như hình ảnh, tên trang bị, mô tả kỹ năng sẽ KHÔNG lưu trong Data Lake để đỡ tốn tiền. Frontend sẽ gọi API trực tiếp sang thư viện của game để lấy (Direct Fetch).

---

## Bạn sẽ học được gì từ dự án này?

Khi hoàn thành series bài viết này, bạn sẽ nắm vững các kỹ năng thực chiến của một **Modern Data Engineer**:

1. **Serverless Orchestration:** Nối ghép Lambda, S3, Glue và EventBridge thành một dây chuyền tự động hoàn toàn mà không cần quản lý một con Server nào.
2. **PySpark ETL:** Thao tác chuyển đổi dữ liệu phức tạp (Flattening Arrays) và áp dụng chuẩn nén Parquet.
3. **Advanced Athena:** Chinh phục kỹ thuật Partition Projection.
4. **Cloud Security & FinOps:** Áp dụng Least Privilege IAM Role và chiến lược tối ưu chi phí (Pay-per-request DynamoDB, Parquet Snappy Compression).


{{% children %}}