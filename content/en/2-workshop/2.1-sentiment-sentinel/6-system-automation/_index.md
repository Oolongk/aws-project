---
weight: 6
date: 2026-03-14
title: "Full Automation with Amazon EventBridge"
chapter: false
pre: "<b>2.1.6. </b>"
---

A Serverless data system is only truly complete when it reaches a "Zero-touch" state — operating automatically without human intervention. In this final chapter, we will set the biological clock for the entire project: automatically wake up and scrape data at 8:00 AM every day, and automatically refresh the report on the Dashboard so stakeholders can view it over their morning coffee.

### Goals of this stage:
1. Configure Amazon EventBridge Scheduler to trigger `Producer_Lambda` daily.
2. Schedule a SPICE memory refresh on AWS QuickSight.

---

### Step 1: Schedule Pipeline Execution with Amazon EventBridge

EventBridge Scheduler is AWS's modern scheduling tool, allowing us to trigger services precisely according to local time zones.

1. Access the **Amazon EventBridge** service on the AWS Console.
2. In the left menu, find *Scheduler* and select **Schedules** -> Click **Create schedule**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-1.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-2.png)

3. **Step 1: Specify schedule detail**
   - **Schedule name:** `Daily-Youtube-Data-Ingestion`
   - **Schedule pattern:** Select *Recurring schedule*.
   - **Schedule type:** Select *Cron-based schedule*.
   - **Cron expression:** Enter `0 8 * * ? *` (equivalent to 8:00 AM every day).
   - **Timezone:** Type and select your timezone, e.g.: `Asia/Ho_Chi_Minh`.
   - Click **Next**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-3.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-4.png)

4. **Step 2: Select target**
   - Select **AWS Lambda**.
   - In the *Lambda function* field, point to your **`Producer_Lambda`** function.
   - Click **Next**.
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-5.png)
![Eventbridge](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/EventBridge-6.png)

5. **Step 3: Settings**
   - Keep all default settings. The system will automatically create a new IAM Role allowing EventBridge to call this Lambda function.
   - Click **Next**, then review the overall configuration and click **Create schedule**.

From this point on, at exactly 8:00 AM (Vietnam time), EventBridge will start the Producer function. Following that, SQS, Consumer, S3, and Transformer Lambda will automatically run in a chain reaction as we set up in the previous chapters. The entire scraping and AI analysis process typically takes about 10-15 minutes.

---

### Step 2: Auto-Refresh Dataset on AWS QuickSight

The new data is already in S3, but QuickSight's SPICE cache needs to be "reminded" to pull this new data up to the Dashboard. Since the Pipeline runs at 8:00 AM and takes about 15 minutes to complete, we will schedule QuickSight to update at **8:30 AM** (to allow ample safe time).

1. Open the **AWS QuickSight** interface.
2. In the left menu, select **Datasets**.
3. Click on the project's Dataset.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-1.png)

4. Switch to the **Refresh** tab -> Click **Add schedule**.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-2.png)
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-3-0.png)

5. Configure the refresh schedule:
   - **Frequency:** Daily.
   - **Timezone:** `Asia/Ho_Chi_Minh`.
   - **Start time:** `08:30`.
![Schedule](/aws-project/images/youtube/6-Tu-dong-hoa-he-thong/Schedule-3.png)

6. Click **Save**.

---

### Series Summary

Congratulations on completing the **AWS Sentiment Sentinel** project!

From a simple list of keywords, we have successfully built a Production-grade Data Pipeline converging all the most cutting-edge technologies:
- **Service Decoupling:** Amazon SQS.
- **Serverless Compute:** AWS Lambda.
- **Data Lake:** Amazon S3 & DynamoDB.
- **Generative AI:** Amazon Bedrock (Claude 3.5 Haiku).
- **Data Analytics:** Amazon Athena & QuickSight.
- **Automation:** Amazon EventBridge.

This project not only demonstrates Python programming ability, but also showcases system architecture thinking, cost-optimization capability, and error handling skills of a professional Data Engineer. The current system can run silently and smoothly for months at near-zero cost (within the AWS Free Tier).