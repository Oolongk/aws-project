---
title: "2.2 Tạo IAM Role & Kích hoạt AI"
date: 2026-03-05
weight: 2
---

Trong AWS, các dịch vụ mặc định bị cách ly và không được phép "nói chuyện" với nhau. Để Lambda có thể gọi AI Bedrock, đọc/ghi file trên S3 và chạy lệnh Athena, chúng ta phải cấp cho nó một "tấm thẻ căn cước" gọi là **IAM Role**.

Bên cạnh đó, chúng ta cũng cần "đánh thức" mô hình Claude 3 trên Amazon Bedrock trước khi đưa vào code.

---

## 1. Kích hoạt Amazon Bedrock (Claude 3 Haiku)

*Tin vui: Từ năm 2026, AWS đã đơn giản hóa tối đa việc cấp quyền mô hình AI bằng cơ chế **Auto-enablement** (Tự động cấp quyền) ở cấp độ tài khoản!*

1. Đăng nhập AWS Console và đảm bảo bạn đang ở Region **N. Virginia (us-east-1)** hoặc **Oregon (us-west-2)**.
2. Truy cập dịch vụ **Amazon Bedrock**.
3. Ở menu bên trái, tìm mục **Playgrounds** và chọn **Chat** (hoặc Text).
4. Bấm vào nút **Select model** -> Chọn nhà cung cấp **Anthropic** -> Chọn **Claude 3 Haiku**.
5. Gõ thử một câu chào (VD: "Hello Claude") và bấm Send. AWS sẽ tự động duyệt và kích hoạt mô hình cho bạn ngay lập tức!

*(Lưu ý nhỏ: Nếu tài khoản của bạn là tài khoản mới tinh và AWS hiện lên một form yêu cầu **Submit use case details**, bạn chỉ cần điền đơn giản: Tên dự án, Website (có thể để link Github), và Mô tả là "Phân tích dữ liệu mạng xã hội cho mục đích học tập" rồi bấm Submit là xong).*

![Test Claude 3 trên Playgrounds](/images/2-Chuan-bi/bedrock-playgrounds-test.png)

---

## 2. Tạo IAM Role cho Ingestor Lambda (Thợ mỏ)

Hàm Ingestor làm nhiệm vụ cào dữ liệu thô và ghi vào Data Lake (S3), đồng thời đánh dấu vào DynamoDB.

1. Truy cập **AWS IAM** -> Chọn **Roles** ở menu bên trái -> Nhấp **Create role**.
2. **Trusted entity type:** Chọn **AWS service**.
3. **Use case:** Chọn **Lambda** -> Nhấp **Next**.
![Tạo IAM role](/images/2-Chuan-bi/IAM-1.png)
4. Ở ô tìm kiếm (Permissions policies), tìm và **tích chọn 3 quyền** sau:
   * `AmazonS3FullAccess`
   * `AmazonDynamoDBFullAccess`
   * `AWSLambdaBasicExecutionRole` (Quyền bắt buộc để ghi log hoạt động).
   * `AmazonSQSFullAccess` 
5. Nhấp **Next** -> Đặt tên Role là `IngestorRole` -> Nhấp **Create role**.
![Tạo IAM role](/images/2-Chuan-bi/IAM-2.png)
![Tạo IAM role](/images/2-Chuan-bi/IAM-3.png)
![Tạo IAM role](/images/2-Chuan-bi/IAM-3-1.png)
   

---

## 3. Tạo IAM Role cho Transformer Lambda (Trái tim AI)

Hàm này cần sức mạnh lớn hơn để gọi AI và kích hoạt Data Catalog của Athena.

1. Lặp lại các bước tạo Role như phần trên (AWS service -> Lambda).
2. Ở ô tìm kiếm, tìm và **tích chọn 4 quyền** sau:
   * `AmazonS3FullAccess` 
   * `AmazonBedrockFullAccess`
   * `AmazonAthenaFullAccess`
   * `AWSLambdaBasicExecutionRole`
3. Nhấp **Next** -> Đặt tên Role là `TransformerRole` -> Nhấp **Create role**.
![Tạo IAM role](/images/2-Chuan-bi/IAM-4.png)
![Tạo IAM role](/images/2-Chuan-bi/IAM-5.png)


![Tạo IAM Role thành công](/images/2-Chuan-bi/IAM-6.png)

**💡 Mẹo bảo mật (Security Best Practice):** Trong môi trường Production của doanh nghiệp, chúng ta sẽ không dùng các quyền `*FullAccess` mà sẽ viết các *Inline Policy* giới hạn quyền truy cập vào đúng một Bucket S3 cụ thể. Tuy nhiên, trong khuôn khổ bài thực hành xây dựng Data Pipeline này, việc dùng Managed Policies sẽ giúp bạn tránh các lỗi "Access Denied" không đáng có.