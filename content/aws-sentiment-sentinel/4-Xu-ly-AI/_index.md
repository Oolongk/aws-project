---
title: "4. Xử lý Dữ liệu và Tích hợp LLM với Amazon Bedrock (Transformation Layer)"
date: 2026-03-12
weight: 4
---

Tại lớp Transformation, dữ liệu JSON thô từ S3 sẽ được phân tích, tóm tắt và dán nhãn cảm xúc tự động. Hệ thống sử dụng kiến trúc Hướng sự kiện (Event-driven) với S3 Trigger để kích hoạt hàm `Transformer_Lambda`. Lõi xử lý ngôn ngữ tự nhiên (NLP) được đảm nhiệm bởi mô hình **Claude 4.5 Haiku** thông qua dịch vụ **Amazon Bedrock**.

### Mục tiêu của chặng này:
1. Cấu hình quyền truy cập mô hình LLM trên Amazon Bedrock.
2. Thiết lập hàm Lambda xử lý dữ liệu và S3 Event Trigger.
3. Triển khai mã nguồn tối ưu hóa chi phí token và xử lý lỗi JSON (Data Chunking & Error Handling).

---

### Bước 1: Kích hoạt mô hình LLM trên Amazon Bedrock

Mặc dù hạ tầng dự án nằm ở Châu Á, luồng xử lý AI sẽ được gọi chéo vùng (Cross-Region Inference) sang khu vực US East (N. Virginia) để tận dụng các mô hình thế hệ mới nhất và giới hạn (quota) tốt nhất.

1. Chuyển Region trên AWS Console sang **US East (N. Virginia) `us-east-1`**.
![Bedrock](/images/4-Xu-ly-AI/Tranform-1.png)
2. Truy cập dịch vụ **Amazon Bedrock** -> Chọn **Model catalog**.
![Bedrock](/images/4-Xu-ly-AI/Bedrock-1.png)
3. Kéo xuống và tìm  **Claude haiku 4.5** và bấm vào.
![Bedrock](/images/4-Xu-ly-AI/Bedrock-2.png)
1. Kéo xuống và tìm mục **Model ID** và copy ID đó lại(sẽ dùng ở bước 3)
![Bedrock](/images/4-Xu-ly-AI/Bedrock-3.png)
---

### Bước 2: Khởi tạo Transformer Lambda và S3 Trigger

Hàm này đóng vai trò là Controller, điều phối dữ liệu từ S3 sang Bedrock và ghi kết quả trở lại S3.

1. Truy cập **AWS Lambda**, tạo hàm mới: `Transformer_Lambda` (Python 3.12), dùng role TransformerRole đã tạo ở mục 2.
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-1.png)
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-2.png)
   
2. **Cấu hình Timeout:** Truy cập tab *Configuration* -> *General configuration* -> Chỉnh Timeout lên mức **15 phút** (đảm bảo đủ thời gian xử lý các file JSON dung lượng lớn).
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-6.png)
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-7.png)
   
3. Tại tab *Code*, chọn **+ Add trigger** để cấu hình luồng sự kiện:
   - **Source:** S3
   - **Bucket:** Chọn Bucket Data Lake.
   - **Event types:** `All object create events`
   - **Prefix:** `raw_data/` *(Bắt buộc để tránh Infinite Loop)*
   - **Suffix:** `.json`
   - Bấm **Add**.
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-3.png)
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-4.png)
![Transformer Lambda](/images/4-Xu-ly-AI/Tranformer-Lambda-5.png)

---

### Bước 3: Triển khai mã nguồn Transformation

Mã nguồn dưới đây giải quyết 3 bài toán lớn khi làm việc với LLM trong môi trường Production:
* **Cost Optimization (Tối ưu chi phí):** Giới hạn token đầu ra bằng cách yêu cầu AI trả về bản tóm tắt (10-15 từ) thay vì dịch toàn văn.
* **Data Chunking (Phân lô dữ liệu):** Chia danh sách bình luận thành các batch nhỏ (15 items/batch) để tránh vượt quá `max_tokens` của Bedrock.
* **JSON Parsing Fallback (Xử lý ngoại lệ):** Xây dựng bộ lọc 3 lớp để bắt và xử lý an toàn các chuỗi JSON bị cắt cụt do AI sinh lỗi.

Triển khai đoạn mã sau vào hàm `Transformer_Lambda` và chọn **Deploy**:

```python
import json
import boto3
import urllib.parse
import time

s3 = boto3.client('s3')
# Chỉ định rõ Region us-east-1 để sử dụng Inference Profile
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1') 

def analyze_sentiment_batch(comments):
    prompt = f"""Bạn là chuyên gia phân tích dữ liệu.
    Đọc các bình luận YouTube dưới đây và thực hiện:
    1. Nhận diện ngôn ngữ gốc.
    2. Đánh giá cảm xúc (TÍCH CỰC, TIÊU CỰC, TRUNG LẬP).
    3. Tóm tắt ý chính bằng Tiếng Việt (tối đa 15 từ). Bỏ qua từ lóng, biểu tượng.

    CHỈ TRẢ VỀ DUY NHẤT 1 MẢNG JSON HỢP LỆ. KHÔNG CÓ MARKDOWN.
    Cấu trúc bắt buộc: "id", "language", "vietnamese_summary", "sentiment".
    
    Dữ liệu đầu vào:
    {json.dumps(comments, ensure_ascii=False)}
    """
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000, 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0 
    })

    try:
        response = bedrock.invoke_model(
            modelId='us.anthropic.claude-3-5-haiku-20241022-v1:0', 
            body=body
        )
        response_body = json.loads(response.get('body').read())
        ai_response_text = response_body['content'][0]['text'].strip()
        
        # Logic phân tích chuỗi JSON an toàn
        start_idx = ai_response_text.find('[')
        end_idx = ai_response_text.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            clean_json = ai_response_text[start_idx:end_idx + 1]
            sentiment_results = json.loads(clean_json)
            
            return {
                item['id']: {
                    'sentiment': item.get('sentiment', 'UNKNOWN'),
                    'language': item.get('language', 'Unknown'),
                    'vietnamese_text': item.get('vietnamese_summary', 'Không có tóm tắt')
                } for item in sentiment_results
            }
        else:
            print(f"[ERROR] Invalid JSON response from LLM: {ai_response_text}")
            return {}
    except Exception as e:
        print(f"[ERROR] Bedrock Invocation Failed: {e}")
        return {}

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        raw_data = json.loads(response['Body'].read().decode('utf-8'))
        
        all_comments = [{"id": item['id'], "text": item['textOriginal']} for item in raw_data.get('items', [])]
        if not all_comments:
            continue
            
        final_analysis_mapping = {}
        batch_size = 15 # Batch limit
        chunks = list(chunk_list(all_comments, batch_size))
        
        for index, chunk in enumerate(chunks):
            mapping = analyze_sentiment_batch(chunk)
            final_analysis_mapping.update(mapping)
            if index < len(chunks) - 1:
                time.sleep(1) # Tránh lỗi Rate Limiting từ Bedrock API
        
        processed_items = []
        for item in raw_data.get('items', []):
            analysis = final_analysis_mapping.get(item['id'], {})
            item['sentiment'] = analysis.get('sentiment', 'KHÔNG XÁC ĐỊNH')
            item['language'] = analysis.get('language', 'Unknown')
            item['vietnamese_text'] = analysis.get('vietnamese_text', 'Lỗi dịch thuật')
            processed_items.append(item)
            
        raw_data['items'] = processed_items
        
        # Di chuyển dữ liệu sang phân vùng processed_data
        path_parts = file_key.split('/') 
        path_parts[0] = 'processed_data' 
        new_file_key = '/'.join(path_parts) 
        
        s3.put_object(Bucket=bucket_name, Key=new_file_key, Body=json.dumps(raw_data, ensure_ascii=False))
        print(f"[SUCCESS] Processed data saved to: {new_file_key}")

    return {'statusCode': 200, 'body': "Transformation Completed."}
```

### Bước 4: Kiểm thử luồng dữ liệu (Pipeline Testing)

Để xác minh toàn bộ luồng Ingestion và Transformation hoạt động đồng bộ:
1. Kích hoạt lại hàm `Producer_Lambda` từ Chương 3 bằng cách chạy Test Event.
2. Giám sát **CloudWatch Logs** của hàm `Transformer_Lambda` để theo dõi tiến trình xử lý batch.
3. Truy cập **Amazon S3**, kiểm tra thư mục `processed_data/`. Tải về một tệp JSON và xác nhận các trường `vietnamese_text`, `language`, `sentiment` đã được gán nhãn thành công.