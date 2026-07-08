---
title : "Cấu hình SQS & Lambda"
date :  "2026-05-13" 
weight : 2
chapter : false
pre : " <b> 2. </b> "
---

#### 1. Tạo hàng đợi Amazon SQS
Amazon SQS đóng vai trò là "giảm xóc" cho hệ thống. Khi hàng ngàn xe tải gửi dữ liệu cùng lúc, SQS sẽ hứng toàn bộ và giữ chúng trong hàng đợi để Lambda xử lý dần dần, tránh gây tràn tải.

1. Tìm kiếm và mở dịch vụ **Simple Queue Service (SQS)**.
2. Nhấn **Create queue**.
3. Cấu hình hàng đợi:
   - **Type**: Chọn **Standard**.
   - **Name**: `IoT_Fleet_Queue`.
4. Giữ các thiết lập mặc định và nhấn **Create queue**.
![Tạo SQS Queue](/aws-project/images/IoTSentinel/2-trien-khai/sqs_create.png?featherlight=false&width=90pc)
5. **Quan trọng**: Sau khi tạo xong, hãy copy **URL** của hàng đợi (có dạng `https://sqs...`) để sử dụng trong bước cấu hình IoT Rule sau này.
![Tạo SQS Queue](/aws-project/images/IoTSentinel/2-trien-khai/sqs_create_2.png?featherlight=false&width=90pc)

---

#### 2. Viết hàm xử lý AWS Lambda
Hàm Lambda này là "bộ não" của hệ thống. Nó sẽ tự động kích hoạt khi có dữ liệu trong SQS, phân tích nhiệt độ và quyết định có gửi cảnh báo hay không.

**Bước A: Tạo hàm Lambda**
1. Mở dịch vụ **Lambda** > Nhấn **Create function**.
2. Chọn **Author from scratch**:
   - **Function name**: `IoT_Process_Data`.
   - **Runtime**: Chọn **Python 3.9** hoặc mới hơn.
3. Nhấn **Create function**.
![Cấp quyền cho Lambda](/aws-project/images/IoTSentinel/2-trien-khai/lambda_create.png?featherlight=false&width=90pc)

**Bước B: Cấp quyền (Permissions)**
Để Lambda có thể đọc SQS, ghi vào DynamoDB và gửi tin qua SNS, bạn cần cấp quyền cho nó:
1. Vào tab **Configuration** > **Permissions** > Nhấn vào tên **Role** để mở giao diện IAM.
![Cấp quyền cho Lambda](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_1.png?featherlight=false&width=90pc)

2. Nhấn **Add permissions** > **Attach policies**.
![Cấp quyền cho Lambda](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_2.png?featherlight=false&width=90pc)

3. Tìm và thêm các quyền: `AmazonSQSFullAccess`, `AmazonDynamoDBFullAccess`, `AmazonSNSFullAccess`.
![Cấp quyền cho Lambda](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_3.png?featherlight=false&width=90pc)



**Bước C: Viết Code xử lý**
Quay lại tab **Code** của Lambda và dán đoạn mã sau (thay thế `YOUR_SNS_TOPIC_ARN` bằng ARN bạn đã copy ở bài 2.1):

```python
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('IoT_Fleet_Data')
SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN' #YOUR_SNS_TOPIC_ARN

def lambda_handler(event, context):
    for record in event['Records']:
        # 1. Đọc dữ liệu từ SQS
        body = json.loads(record['body'], parse_float=Decimal)
        truck_id = body['truck_id']
        temp = body['temperature']
        
        # 2. Kiểm tra điều kiện nhiệt độ (> 8 độ C)
        if temp > Decimal('8.0'):
            message = f"CẢNH BÁO: Xe {truck_id} có nhiệt độ bất thường: {temp}°C!"
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="Cảnh báo nhiệt độ vắc-xin")
        
        # 3. Lưu vào DynamoDB
        table.put_item(Item=body)
        
    return {'statusCode': 200, 'body': 'Xử lý thành công'}
```

**Bước D: Thêm Trigger**
1. Nhấn **Add trigger** > Chọn **SQS**.
![Thêm Trigger SQS](/aws-project/images/IoTSentinel/2-trien-khai/lambda_trigger_1.png?featherlight=false&width=90pc)

2. Chọn hàng đợi `IoT_Fleet_Queue` vừa tạo.
![Thêm Trigger SQS](/aws-project/images/IoTSentinel/2-trien-khai/lambda_trigger_2.png?featherlight=false&width=90pc)
3. Nhấn **Add**.
