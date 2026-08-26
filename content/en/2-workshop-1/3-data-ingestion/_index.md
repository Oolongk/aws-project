---
weight: 3
date: 2026-03-12
title: "Data Ingestion Layer with AWS SQS & Lambda"
chapter: false
pre: "<b>2.1.3. </b>"
---

Welcome to the first critical stage: Building the Data Collection Pipeline. Instead of a bulky monolithic design, we will build a **Decoupled** architecture using **Amazon SQS** as a buffer between "finding videos" and "scraping comments".

### Goals of this stage:
1. Create a queue using AWS SQS.
2. Write the `Producer_Lambda` function to find top trending videos and push IDs to the queue.
3. Write the `Ingestor_Lambda` function to read IDs from the queue, deep-paginate comments, and save to the S3 Data Lake.

---

### Step 1: Create State Database (Amazon DynamoDB)
We need 2 notebooks so the Lambda system does not "lose memory" after each run.

1. Access the **DynamoDB** service on AWS Console.
2. Click **Create table** to create the first table (Comment tracking notebook):
   - **Table name:** `YoutubeCommentsTracker`
   - **Partition key:** `comment_id` (Data type: *String*)
![Create DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-1.png)
   - Click **Create table**.
![Create DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-2.png)

1. Continue clicking **Create table** to create the second table (Error video blacklist):
   - **Table name:** `YoutubeVideoBlacklist`
   - **Partition key:** `video_id` (Data type: *String*)
   - Click **Create table**.
![Create DynamoDB](/aws-project/images/youtube/3-Thu-thap-du-lieu/Dynamo-3.png)

---

### Step 2: Create the Amazon SQS Queue
SQS (Simple Queue Service) acts as a shock absorber. If YouTube returns too many videos, SQS will hold them back so the system can process them gradually, preventing overload.

1. Access **Amazon SQS** on the AWS Console.
2. Select **Create queue**.
3. Choose type **Standard**.
4. Name it: `YoutubeVideoQueue`.
![Create SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-1.png)

5. Keep the default settings and click **Create queue**.
![Create SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-2.png)

6. **Note:** Copy the Queue `URL` for use in the next step.
![Create SQS](/aws-project/images/youtube/3-Thu-thap-du-lieu/SQS-3.png)

---

### Step 3: Build Producer Lambda
This function searches for videos based on a keyword list. To optimize cost and avoid exhausting the API Quota, we limit to 3 top videos per keyword and check against the "Blacklist" before sending.

1. Access **AWS Lambda**, create a new function named `Producer_Lambda` (Python 3.x).
2. Attach the `IngestorRole` created in part 2 (it already has access to DynamoDB and SQS, so no new role is needed).
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-2.png)

3. Set the **timeout** to give **Producer** enough running time.
   ![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-1.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-2.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-3.png)
4. Add Environment Variable: `YOUTUBE_API_KEY`.

![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-4.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-5.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-6.png)
![Create Producer](/aws-project/images/youtube/3-Thu-thap-du-lieu/Producer_Lambda-7.png)

4. Paste the following code and click **Deploy**:

```python
import json
import boto3
import urllib.request
import urllib.parse
import os

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
blacklist_table = dynamodb.Table('YoutubeVideoBlacklist')

# Replace with your Queue URL from Step 2
QUEUE_URL = 'https://sqs.<region>.amazonaws.com/<account-id>/YoutubeVideoQueue'

def get_video_ids_by_keyword(api_key, query, max_results=3):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={encoded_query}&key={api_key}&maxResults={max_results}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        return [item['id']['videoId'] for item in data.get('items', []) if item['id'].get('videoId')]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def lambda_handler(event, context):
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    keywords = ["review iphone 16", "review electric car", "review laptop 2026", "review RE9"]
    all_video_ids = []
    
    # Fetch 3 videos per keyword (total 12 videos)
    for kw in keywords:
        ids = get_video_ids_by_keyword(API_KEY, kw) 
        all_video_ids.extend(ids)
        
    unique_video_ids = list(set(all_video_ids))
    pushed_count = 0
    
    for vid in unique_video_ids:
        # Check Blacklist to skip videos that previously errored (e.g., comments disabled)
        db_response = blacklist_table.get_item(Key={'video_id': vid})
        if 'Item' in db_response:
            continue 
            
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps({"video_id": vid}))
        pushed_count += 1
        
    return {'statusCode': 200, 'body': f"Scanned and pushed {pushed_count} videos safely to SQS."}
```

---

### Step 4: Build Ingestor Lambda
This function is automatically triggered (Triggered) every time a message arrives in SQS. It uses **Pagination** to deep-dig comments, while cross-checking with DynamoDB to ensure **duplicate data is never collected**.

1. Create a new Lambda function: `Ingestor_Lambda`.
2. In the **Add trigger** section, select source **SQS**, pointing to the `YoutubeVideoQueue` just created.
![Add Trigger](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-Ingestor-1.png)
![Add Trigger](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-Ingestor-2.png)
![Add Trigger](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-Ingestor-3.png)

3. Set the **timeout** to give **Ingestor** enough running time.
![Timeout](/aws-project/images/youtube/3-Thu-thap-du-lieu/Lambda-Ingestor-1-1.png)

4. Paste the optimized scraping code below:

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

BUCKET_NAME = 'your-datalake-bucket-name' # Replace with your Bucket name

def get_comments_for_video(api_key, video_id, target_new_comments=50, max_pages=10):
    new_items = []
    next_page_token = ""
    pages_searched = 0
    
    # Loop deep until 50 new comments are found OR all pages are exhausted
    while len(new_items) < target_new_comments and pages_searched < max_pages:
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=50"
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
                
                # Only process if comment has never existed in Tracker
                if 'Item' not in db_response:
                    snippet = item['snippet']['topLevelComment']['snippet']
                    new_items.append({
                        'id': comment_id,
                        'authorDisplayName': snippet.get('authorDisplayName', 'Unknown'),
                        'textOriginal': snippet.get('textOriginal', ''),
                        'publishedAt': snippet.get('publishedAt', '')
                    })
                    # Mark as scraped in DB
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
        
        # Only save S3 file if there is actually NEW data
        if len(payload['items']) > 0:
            now = datetime.now()
            file_name = f"comments_{vid}_{int(now.timestamp())}.json"
            s3_key = f"raw_data/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}/{file_name}"
            
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=json.dumps(payload, ensure_ascii=False))
            
    return {'statusCode': 200, 'body': "Consumer processing complete."}
```

### Step 5: Configure Test Event and Run System Test

To trigger the system for the first time, we need to create a seed event (Test Event) for the Producer function. Since this function already has a keyword list in the code, this Test Event is purely procedural.

1. Open the **`Producer_Lambda`** function on the AWS Console.
2. Click the small arrow next to the blue **Test** button (or select the **Test** tab).
3. Select **Configure test event**.
4. Fill in the following:
   - **Event name:** `TestProducer`
   - **Event JSON:** You can keep the default AWS code, or clear it and leave an empty brace `{}`.
5. Click **Save**.
6. Now, take a deep breath and click the blue **Test** button!

### Results
Within a few minutes, the system will automatically scan, push to the queue, deep-dig data and save neatly to the `raw_data/` folder in the S3 Data Lake. This architecture ensures the system never re-scrapes old data, optimizing all AWS resource costs.