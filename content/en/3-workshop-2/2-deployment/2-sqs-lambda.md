---
weight: 2
date: "2026-05-13"
title: "Create Amazon SQS & Write AWS Lambda"
chapter: false
pre: "<b>2.2.2.2. </b>"
---

#### 1. Create Amazon SQS Queue
Amazon SQS acts as the "shock absorber" for the system. When thousands of trucks send data simultaneously, SQS will buffer all of it and hold the messages in the queue for Lambda to process gradually, preventing overload.

1. Search for and open the **Simple Queue Service (SQS)** service.
2. Click **Create queue**.
3. Configure the queue:
   - **Type**: Select **Standard**.
   - **Name**: `IoT_Fleet_Queue`.
4. Keep the default settings and click **Create queue**.
![Create SQS Queue](/aws-project/images/IoTSentinel/2-trien-khai/sqs_create.png?featherlight=false&width=90pc)
5. **Important**: After creation, copy the queue **URL** (in the format `https://sqs...`) for use in the IoT Rule configuration step later.
![Create SQS Queue](/aws-project/images/IoTSentinel/2-trien-khai/sqs_create_2.png?featherlight=false&width=90pc)

---

#### 2. Write the AWS Lambda Processing Function
This Lambda function is the "brain" of the system. It will automatically trigger when data is in SQS, analyze the temperature, and decide whether to send an alert.

**Step A: Create the Lambda Function**
1. Open the **Lambda** service > Click **Create function**.
2. Select **Author from scratch**:
   - **Function name**: `IoT_Process_Data`.
   - **Runtime**: Select **Python 3.9** or newer.
3. Click **Create function**.
![Grant Lambda permissions](/aws-project/images/IoTSentinel/2-trien-khai/lambda_create.png?featherlight=false&width=90pc)

**Step B: Grant Permissions**
For Lambda to read from SQS, write to DynamoDB, and send messages via SNS, you need to grant it permissions:
1. Go to the **Configuration** tab > **Permissions** > Click the **Role** name to open the IAM interface.
![Grant Lambda permissions](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_1.png?featherlight=false&width=90pc)

2. Click **Add permissions** > **Attach policies**.
![Grant Lambda permissions](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_2.png?featherlight=false&width=90pc)

3. Find and add the permissions: `AmazonSQSFullAccess`, `AmazonDynamoDBFullAccess`, `AmazonSNSFullAccess`.
![Grant Lambda permissions](/aws-project/images/IoTSentinel/2-trien-khai/lambda_iam_3.png?featherlight=false&width=90pc)

**Step C: Write the Processing Code**
Return to the **Code** tab of Lambda and paste the following code (replace `YOUR_SNS_TOPIC_ARN` with the ARN you copied in lesson 2.1):

```python
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('IoT_Fleet_Data')
SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN' # Replace with your SNS Topic ARN

def lambda_handler(event, context):
    for record in event['Records']:
        # 1. Read data from SQS
        body = json.loads(record['body'], parse_float=Decimal)
        truck_id = body['truck_id']
        temp = body['temperature']
        
        # 2. Check temperature condition (> 8 degrees C)
        if temp > Decimal('8.0'):
            message = f"ALERT: Truck {truck_id} has abnormal temperature: {temp}°C!"
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="Vaccine Temperature Alert")
        
        # 3. Save to DynamoDB
        table.put_item(Item=body)
        
    return {'statusCode': 200, 'body': 'Processing successful'}
```

**Step D: Add Trigger**
1. Click **Add trigger** > Select **SQS**.
![Add SQS Trigger](/aws-project/images/IoTSentinel/2-trien-khai/lambda_trigger_1.png?featherlight=false&width=90pc)

2. Select the `IoT_Fleet_Queue` queue just created.
![Add SQS Trigger](/aws-project/images/IoTSentinel/2-trien-khai/lambda_trigger_2.png?featherlight=false&width=90pc)
3. Click **Add**.