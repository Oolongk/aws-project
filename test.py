import os

# Danh sách toàn bộ các file cần tạo trong dự án
files_to_create = [
    "content/clickstream-project/_index.md",
    
    "content/clickstream-project/1-ingestion-layer/_index.md",
    "content/clickstream-project/1-ingestion-layer/1.1-s3-glue-setup.md",
    "content/clickstream-project/1-ingestion-layer/1.2-kinesis-firehose.md",
    "content/clickstream-project/1-ingestion-layer/1.3-data-simulator.md",
    
    "content/clickstream-project/2-orchestration-etl/_index.md",
    "content/clickstream-project/2-orchestration-etl/2.1-step-functions.md",
    "content/clickstream-project/2-orchestration-etl/2.2-lambda-athena-etl.md",
    
    "content/clickstream-project/3-ai-recommender/_index.md",
    "content/clickstream-project/3-ai-recommender/3.1-amazon-personalize.md",
    
    "content/clickstream-project/4-project-cleanup/_index.md",
    "content/clickstream-project/4-project-cleanup/4.1-clean-up-all-services.md"
]

print("Bắt đầu khởi tạo cây thư mục...\n")

for file_path in files_to_create:
    # Trích xuất đường dẫn thư mục từ đường dẫn file
    directory = os.path.dirname(file_path)
    
    # Tạo thư mục cha nếu chưa tồn tại
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Tạo file trống (không ghi nội dung)
    with open(file_path, "w", encoding="utf-8") as file:
        pass 
        
    print(f"📄 Đã tạo: {file_path}")

print("\n✅ HOÀN TẤT! Toàn bộ cây thư mục và file đã được tạo thành công.")