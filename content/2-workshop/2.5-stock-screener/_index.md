---
title: "Quantamental Stock Screener Time-Series Pipeline"
date: 2026-07-08
weight: 2
chapter: true
pre: "Project 2 "
---

# Quantamental Stock Screener Time-Series Pipeline

US Stock Screener Pipeline là dự án Data Engineering xây dựng hệ thống thu thập, chuẩn hóa, tính điểm **Quality Minus Junk (QMJ)** cho cổ phiếu S&P 500 và hiển thị kết quả trên Web Frontend.

Mục tiêu của dự án không chỉ là lấy dữ liệu giá cổ phiếu. Pipeline phải duy trì được dữ liệu lịch sử, tách rõ Raw Data và Processed Data, đồng thời tạo một Serving Layer để người dùng tra cứu kết quả QMJ theo từng mã cổ phiếu.

## Mục tiêu dự án

| Mục tiêu | Cách dự án xử lý |
|---|---|
| Thu thập dữ liệu cổ phiếu S&P 500 | Lấy danh sách ticker từ Wikipedia và dữ liệu thị trường từ Yahoo Finance thông qua `yfinance` |
| Xây dựng dữ liệu lịch sử | Local Backfill Script lấy dữ liệu giá từ năm 2023 và ghi theo ngày giao dịch thực tế |
| Cập nhật dữ liệu hằng ngày | AWS Glue Python Shell lấy phiên giá mới nhất, Company Info và Financials snapshot |
| Chuẩn hóa dữ liệu đầu vào | Ép schema, chuyển tên cột về `snake_case`, ép metric về `float64` và date fields về `string` |
| Tính điểm định lượng | AWS Glue PySpark tính profitability, growth, safety, value, momentum và QMJ score |
| Cung cấp dữ liệu cho Web | Lambda QMJ Loader nạp Processed Parquet vào DynamoDB; Lambda Reader trả dữ liệu cho API và Frontend |

## Kết quả đầu ra

Sau khi hoàn thành pipeline, hệ thống tạo ba lớp dữ liệu chính:

| Lớp dữ liệu | Vị trí | Vai trò |
|---|---|---|
| Raw Zone | `s3://stock-screener-raw-tên-của-bạn/raw_us_market/` | Lưu dữ liệu gốc đã chuẩn hóa từ Backfill và Daily Ingestion |
| Processed Zone | `s3://stock-screener-processed-tên-của-bạn/processed_qmj/as_of_date=YYYY-MM-DD/` | Lưu Parquet đã tính QMJ, xếp hạng cổ phiếu và các score thành phần |
| Serving Store | DynamoDB table `qmj_screener` | Lưu projection theo `ticker` và `snapshot_date` để API truy vấn nhanh |

Người dùng có thể nhập ticker, ví dụ `AAPL`, trên Web Frontend để xem lịch sử điểm QMJ và các chỉ số phục vụ việc sàng lọc cổ phiếu.


![Kiến trúc US Stock Screener Pipeline](/images/stock-screener/diagram.jpg?featherlight=false&width=90pc)

## Các lớp trong kiến trúc

| Layer | Thành phần | Trách nhiệm |
|---|---|---|
| Data Sources | Wikipedia, Yahoo Finance, yfinance | Cung cấp ticker S&P 500, giá, Company Info và Financials |
| Ingestion Layer | Local Backfill Script, Glue Python Shell | Nạp lịch sử và cập nhật dữ liệu hằng ngày vào Raw Zone |
| Storage Layer | Amazon S3 Raw Zone, Amazon S3 Processed Zone | Lưu dữ liệu Parquet Snappy theo từng giai đoạn xử lý |
| Processing Layer | AWS Glue PySpark | Làm sạch, deduplicate, tính metric và QMJ ranking |
| Serving Layer | S3 Event Notification, Lambda QMJ Loader, DynamoDB | Chuyển analytical dataset thành dữ liệu tối ưu cho API |
| Presentation Layer | Lambda Reader, API Gateway, Static Web Frontend | Cung cấp API và hiển thị thông tin QMJ cho người dùng |

## Bộ dữ liệu chính

| Dataset | Mô tả | Nguồn tạo |
|---|---|---|
| `us_prices_raw.parquet` | Giá giao dịch theo ticker và `price_date` | Local Backfill và Glue Python Shell |
| `us_company_info.parquet` | Snapshot thông tin doanh nghiệp | Local Backfill và Glue Python Shell |
| `us_financials_raw.parquet` | Báo cáo tài chính quarterly hoặc annual | Glue Python Shell |
| QMJ Processed Parquet | QMJ score, rank, profitability, growth, safety, value và momentum | Glue PySpark Transform |
| `qmj_screener` | Bản dữ liệu phục vụ API theo `ticker` và `snapshot_date` | Lambda QMJ Loader |

## Nguyên tắc thiết kế

| Nguyên tắc | Cách áp dụng trong dự án |
|---|---|
| Schema parity | Backfill và Daily Ingestion chuẩn hóa cùng tên cột, kiểu dữ liệu và định dạng date trước khi ghi Parquet |
| Partitioning | Prices lưu theo ngày giao dịch; Company Info và Financials lưu theo ngày chạy pipeline |
| Reprocessing | Có thể chạy lại Glue Transform từ Raw Zone khi thay đổi công thức QMJ mà không cần crawl lại dữ liệu nguồn |
| Idempotent serving write | Lambda Loader dùng `ticker` và `snapshot_date` làm khóa ghi đè để giảm bản ghi trùng trên DynamoDB |
| Separation of concerns | S3 Processed là analytical source of truth; DynamoDB chỉ là serving projection cho Web/API |

## Phạm vi tài liệu

Tài liệu này hướng dẫn triển khai dự án theo các phase sau:

| Chương | Nội dung |
|---|---|
| Chương 1 | Chuẩn bị AWS resources, S3 zones, IAM Roles và data contract |
| Chương 2 | Local Backfill và Glue Python Shell Daily Ingestion |
| Chương 3 | Glue PySpark QMJ Transformation |
| Chương 4 | Lambda QMJ Loader, DynamoDB, Lambda Reader, API Gateway và Web Frontend |
| Chương 5 | Automation, monitoring, kiểm thử và cleanup resources |

{{% children %}}
