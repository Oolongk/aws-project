---
title: "3. Thu thập dữ liệu (Ingestion Layer) với AWS SQS & Lambda"
date: 2026-03-12
weight: 3
---

Chào mừng các bạn đến với chặng quan trọng đầu tiên: Xây dựng đường ống thu thập dữ liệu (Data Pipeline). Thay vì một thiết kế nguyên khối (Monolithic) cồng kềnh, chúng ta sẽ xây dựng kiến trúc **Decoupled (Tách rời)** bằng cách dùng **Amazon SQS** làm vùng đệm giữa việc "tìm video" và "cào bình luận".

### Mục tiêu của chặng này:
1. Tạo một hàng đợi (Queue) bằng AWS SQS.
2. Viết hàm `Producer_Lambda` để tìm top video trending và đẩy ID vào hàng đợi.
3. Viết hàm `Ingestor_Lambda` để đọc ID từ hàng đợi, đào sâu bình luận (Pagination) và lưu vào S3 Data Lake.

---

### Bước 1: Tạo cơ sở dữ liệu trạng thái (Amazon DynamoDB)
Chúng ta cần 2 cuốn sổ ghi chép để hệ thống Lambda không bị "mất trí nhớ" sau mỗi lần chạy.

1. Truy cập dịch vụ **DynamoDB** trên AWS Console.
2. Bấm **Create table** để tạo bảng thứ nhất (Sổ theo dõi bình luận):
   - **Table name:** `YoutubeCommentsTracker`  
   - **Partition key:** `comment_id` (Kiểu dữ liệu: *String*)
![Tạo DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-1.png)
   - Bấm **Create table**.
![Tạo DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-2.png)
   
1. Tiếp tục bấm **Create table** để tạo bảng thứ hai (Sổ đen video lỗi):
   - **Table name:** `YoutubeVideoBlacklist`
   - **Partition key:** `video_id` (Kiểu dữ liệu: *String*)
   - Bấm **Create table**.
![Tạo DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-3.png)

---

### Bước 2: Tạo "Băng chuyền" Amazon SQS
SQS (Simple Queue Service) sẽ đóng vai trò như một hệ thống giảm xóc. Nếu YouTube trả về quá nhiều video, SQS sẽ giữ chúng lại để hệ thống từ từ xử lý, tránh quá tải.

1. Truy cập vào **Amazon SQS** trên AWS Console.
2. Chọn **Create queue**.
3. Chọn loại **Standard** (Tiêu chuẩn).
4. Đặt tên: `YoutubeVideoQueue`.
![Tạo SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-1.png)
   
5. Giữ nguyên các thông số mặc định và bấm **Create queue**.
![Tạo SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-2.png)
   
6. **Lưu ý:** Hãy copy lại đường link `URL` của Queue này để dùng cho bước sau.
![Tạo SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-3.png)
   

---

### Bước 3: Xây dựng Producer Lambda (Khóa van đầu nguồn)
Hàm này có nhiệm vụ tìm kiếm video dựa trên danh sách từ khóa. Để tối ưu chi phí và tránh cạn kiệt API Quota, chúng ta sẽ giới hạn chỉ lấy 3 video top đầu cho mỗi từ khóa và kiểm tra qua "Sổ đen" (Blacklist) trước khi gửi đi.


1. Truy cập **AWS Lambda**, tạo hàm mới tên là `Producer_Lambda` (Python 3.x).
2. Gắn quyền (Role) `IngestorRole` đã tạo ở phần 2(vì nó có quyền truy cập vào Dynamo và SQS nên tận dùng lại ko cần phải tạo 1 role mới).
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-2.png)

3. Cài đặt **timeout** để **Producer** có thời gian chạy.

   ![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-1.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-2.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-3.png)
4. Thêm Environment Variable: `YOUTUBE_API_KEY`.

![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-4.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-5.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-6.png)
![Tạo Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-7.png)
   
4. Dán đoạn code sau và bấm **Deploy**:

```python
import json
import boto3
import urllib.request
import urllib.parse
import os

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
blacklist_table = dynamodb.Table('YoutubeVideoBlacklist')

# Thay bằng URL Queue của bạn ở Bước 2
QUEUE_URL = 'https://sqs.<region>[.amazonaws.com/](https://.amazonaws.com/)<account-id>/YoutubeVideoQueue'

def get_video_ids_by_keyword(api_key, query, max_results=3):
    encoded_query = urllib.parse.quote(query)
    url = f"[https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=](https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=){encoded_query}&key={api_key}&maxResults={max_results}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        return [item['id']['videoId'] for item in data.get('items', []) if item['id'].get('videoId')]
    except Exception as e:
        print(f"❌ Lỗi tìm kiếm: {e}")
        return []

def lambda_handler(event, context):
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    keywords = ["review iphone 16", "review xe điện", "review laptop 2026", "review RE9"]
    all_video_ids = []
    
    # Lấy 3 video cho mỗi từ khóa (tổng 12 videos)
    for kw in keywords:
        ids = get_video_ids_by_keyword(API_KEY, kw) 
        all_video_ids.extend(ids)
        
    unique_video_ids = list(set(all_video_ids))
    pushed_count = 0
    
    for vid in unique_video_ids:
        # Kiểm tra Blacklist để bỏ qua các video từng bị lỗi (vd: tắt comment)
        db_response = blacklist_table.get_item(Key={'video_id': vid})
        if 'Item' in db_response:
            continue 
            
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps({"video_id": vid}))
        pushed_count += 1
        
    return {'statusCode': 200, 'body': f"Đã quét và đẩy {pushed_count} videos an toàn vào SQS."}
```

---

### Bước 4: Xây dựng Ingestor Lambda (Thợ mỏ cừ khôi)
Hàm này sẽ được kích hoạt (Trigger) tự động mỗi khi có tin nhắn rơi vào SQS. Nó sử dụng kỹ thuật **Pagination (Phân trang)** để đào sâu lấy bình luận, đồng thời kiểm tra chéo với DynamoDB để đảm bảo **không bao giờ lấy trùng dữ liệu cũ**.

1. Tạo hàm Lambda mới: `Ingestor_Lambda`.
2. Trong phần **Add trigger**, chọn nguồn là **SQS**, trỏ đến `YoutubeVideoQueue` vừa tạo.
![Add Trigger](/aws-project/images/3-Thu-thap-du-lieu/Lambda-Ingestor-1.png)
![Add Trigger](/aws-project/images/3-Thu-thap-du-lieu/Lambda-Ingestor-2.png)
![Add Trigger](/aws-project/images/3-Thu-thap-du-lieu/Lambda-Ingestor-3.png)
   
3. Cài đặt **timeout** để **Ingestor** có thời gian chạy.
![Timeout](/aws-project/images/3-Thu-thap-du-lieu/Lambda-Ingestor-1-1.png)
   
4. Dán đoạn code cào dữ liệu tối ưu dưới đây:

```python
import json
import boto3
import urllib.request
import os
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
tracker_table = dynamodb.Table('YoutubeCommentsTracker')
blacklist_table = dynamodb.Table('YoutubeVideoBlacklist')

BUCKET_NAME = 'ten-bucket-datalake-cua-ban' # Thay tên Bucket của bạn

def get_comments_for_video(api_key, video_id, target_new_comments=50, max_pages=10):
    new_items = []
    next_page_token = ""
    pages_searched = 0
    
    # Vòng lặp đào sâu đến khi đủ 50 comment mới HOẶC hết trang
    while len(new_items) < target_new_comments and pages_searched < max_pages:
        url = f"[https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=](https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=){video_id}&key={api_key}&maxResults=50"
        if next_page_token:
            url += f"&pageToken={next_page_token}"
            
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            items = data.get('items', [])
            if not items:
                break 
                
            for item in items:
                if len(new_items) >= target_new_comments:
                    break
                    
                comment_id = item['id']
                db_response = tracker_table.get_item(Key={'comment_id': comment_id})
                
                # Chỉ xử lý nếu comment chưa từng tồn tại trong Tracker
                if 'Item' not in db_response:
                    snippet = item['snippet']['topLevelComment']['snippet']
                    new_items.append({
                        'id': comment_id,
                        'authorDisplayName': snippet.get('authorDisplayName', 'Unknown'),
                        'textOriginal': snippet.get('textOriginal', ''),
                        'publishedAt': snippet.get('publishedAt', '')
                    })
                    # Đánh dấu đã cào vào DB
                    tracker_table.put_item(Item={'comment_id': comment_id, 'video_id': video_id})
                    
            next_page_token = data.get('nextPageToken')
            pages_searched += 1
            if not next_page_token:
                break
                
        except Exception as e:
            if pages_searched == 0:
                blacklist_table.put_item(Item={'video_id': video_id, 'reason': str(e)})
            break 
            
    return {"video_id": video_id, "items": new_items}

def lambda_handler(event, context):
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    
    for record in event['Records']:
        body = json.loads(record['body'])
        vid = body['video_id']
        
        payload = get_comments_for_video(API_KEY, vid) 
        
        # Chỉ lưu file S3 nếu thực sự có dữ liệu MỚI
        if len(payload['items']) > 0:
            now = datetime.now()
            file_name = f"comments_{vid}_{int(now.timestamp())}.json"
            s3_key = f"raw_data/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}/{file_name}"
            
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=json.dumps(payload, ensure_ascii=False))
            
    return {'statusCode': 200, 'body': "Hoàn tất xử lý Consumer."}
```
### Bước 5: Cấu hình Test Event và Chạy thử nghiệm hệ thống

Để kích hoạt hệ thống chạy lần đầu tiên, chúng ta cần tạo một sự kiện mồi (Test Event) cho hàm Producer. Vì hàm này đã có sẵn danh sách từ khóa trong code nên Test Event này chỉ mang tính chất thủ tục.

1. Mở hàm **`Producer_Lambda`** trên AWS Console.
2. Bấm vào mũi tên nhỏ bên cạnh nút **Test** màu xanh nước biển (hoặc chọn tab **Test**).
3. Chọn **Configure test event**.
4. Điền các thông tin sau:
   - **Event name:** `TestProducer`
   - **Event JSON:** Bạn có thể giữ nguyên đoạn code mặc định của AWS, hoặc xóa hết và để một ngoặc nhọn rỗng `{}`.
5. Bấm **Save** để lưu lại.
6. Bây giờ, hãy hít một hơi thật sâu và bấm nút **Test** màu xanh!

### Kết quả đạt được
 Chỉ sau vài phút, hệ thống sẽ tự động quét, đẩy vào hàng đợi, đào sâu dữ liệu và lưu gọn gàng vào thư mục `raw_data/` trên S3 Data Lake. Kiến trúc này đảm bảo hệ thống không bao giờ cào lại dữ liệu cũ, tối ưu hóa toàn bộ chi phí tài nguyên AWS.