---
title: "2.3 Xây dựng Data Lake với Amazon S3"
date: 2026-03-05
weight: 3
---

Trong kiến trúc chuẩn của Data Engineer, chúng ta sẽ xây dựng một Data Lake trung tâm bằng **Amazon S3**. Thay vì tạo nhiều Bucket rời rạc, chúng ta sẽ dùng **1 Bucket duy nhất** và chia thành các thư mục (Folders) theo mô hình quản lý dữ liệu đa tầng.

---

### Bước 1: Tạo S3 Bucket

*Lưu ý: Tên Bucket trên AWS phải là duy nhất trên toàn cầu.*

1. Đăng nhập AWS Console và truy cập **Amazon S3**.
2. Bấm nút màu cam **Create bucket**.
3. **Bucket name:** Nhập tên theo cấu trúc `social-sentiment-datalake-tencuaban` (Thay *tencuaban* bằng tên hoặc MSSV của bạn).
4. Giữ nguyên tất cả cài đặt mặc định (đặc biệt là tính năng chặn truy cập công cộng *Block all public access*).
5. Kéo xuống dưới cùng và bấm **Create bucket**.
![Cấu trúc thư mục S3](/images/2-Chuan-bi/S3-1.png)
![Cấu trúc thư mục S3](/images/2-Chuan-bi/S3-2.png)
   

### Bước 2: Tạo các Thư mục (Data Layers)

Bấm vào Bucket vừa tạo, sau đó bấm nút **Create folder** để tạo lần lượt 3 thư mục sau:

1. **`raw_data`**: Vùng chứa dữ liệu thô sơ (Bronze Layer) do hàm Ingestor cào trực tiếp từ YouTube về.
2. **`processed_data`**: Vùng chứa dữ liệu đã làm sạch và được AI gắn nhãn cảm xúc (Silver Layer).
3. **`athena_results`**: Thư mục kỹ thuật bắt buộc để lưu file log mỗi khi AWS Athena chạy lệnh truy vấn.

![Cấu trúc thư mục S3](/images/2-Chuan-bi/S3-3.png)

