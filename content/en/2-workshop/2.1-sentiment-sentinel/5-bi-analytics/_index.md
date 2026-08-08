---
weight: 5
date: 2026-03-14
title: "Data Visualization: Amazon Athena and AWS QuickSight"
chapter: false
pre: "<b>2.1.5. </b>"
---

The final step of the Data Pipeline architecture is the Presentation Layer. Instead of building complex ETL flows to load data into a traditional Database, the system uses **Amazon Athena** to query JSON files directly on S3 using SQL (Schema-on-read architecture). The data is then pushed into the SPICE memory of **Amazon QuickSight** to build a BI Dashboard.

### Goals of this stage:
1. Define the data schema using Amazon Athena (UI Query Editor v3).
2. Configure unified IAM Security permissions for QuickSight.
3. Build a user sentiment monitoring Dashboard.

---

### Step 1: Initialize Schema with Amazon Athena

Amazon Athena allows direct reading of raw data on S3 without operating a server (Serverless SQL).

1. Access the **Amazon Athena** service on the AWS Console.
2. **Configure Output Location (Required):**
   - From the left menu, select **Query editor**
   - On the Editor v3 screen, look to the right and select the **Query Settings** tab -> Click **Manage**.
   - In the *Query result location* field, specify an S3 path for storing query logs (the athena_result folder created in section 2). Click **Save**.
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-0.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-1.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-2.png)
![Athena](/aws-project/images/youtube/4-Xu-ly-AI/Athena-3.png)

1. Return to the **Editor** tab, run the following DDL command to create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS sentiment_db;
   ```
2. Select the `sentiment_db` database just created in the left *Database* panel.
3. Run the following SQL command to define the table, mapping directly to the processed data folder on S3:
   ```sql
   CREATE EXTERNAL TABLE IF NOT EXISTS youtube_comments (
     `id` string,
     `language` string,
     `vietnamese_text` string,
     `sentiment` string
   )
   ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
   LOCATION 's3://<your-bucket>/processed_data/';
   ```
   *(Note: Replace `<your-bucket>` with the actual Data Lake Bucket name of the project.)*
4. Run a test query to confirm data was loaded successfully:
   ```sql
   SELECT * FROM youtube_comments LIMIT 10;
   ```

---

### Step 2: Build Normalized View

Instead of exposing the raw table (`youtube_comments_raw`) to QuickSight, we will create a **View**. This layer renames columns to be business-user-friendly and filters out error records (if any) to conserve SPICE capacity.

In the Athena Editor tab, run the following SQL command:

```sql
CREATE OR REPLACE VIEW vw_youtube_sentiment AS
SELECT 
    id AS comment_id,
    UPPER(language) AS source_language,
    vietnamese_text AS translated_summary,
    UPPER(sentiment) AS sentiment_label
FROM youtube_comments_raw
WHERE sentiment IS NOT NULL 
  AND sentiment != 'UNKNOWN'
  AND sentiment != 'UNDEFINED';
```
Now, QuickSight will only work with this clean `vw_youtube_sentiment` View.

---

### Step 3: Grant S3 Access to QuickSight

This is an important security configuration step. QuickSight's 2026 Security interface requires administrators to explicitly grant Write permissions to the Athena Workgroup to prevent `AccessDenied` errors when loading charts.

1. Access the **QuickSight** service. *(Register a Standard/Enterprise account if this is your first time accessing it.)*
2. On the main interface, click the Avatar icon (top right corner) -> Select **Manage QuickSight**.
3. In the left navigation menu, select **AWS Resources**.
5. Configure access permissions (IAM Policies):
   - Check **Amazon Athena**. Click *Next* on the popup that appears.
   - Check **Amazon S3**. A list of Buckets will appear.
   - **IMPORTANT STEP:** Find and check your Data Lake Bucket to grant Read permission. You must also check the **Write permission for Athena Workgroup** box in the adjacent column so QuickSight has permission to write query result logs.
6. Click **Save**.
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-1.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-2.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-3.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-4.png)
![QuickSight](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-5.png)

---

### Step 4: Load Data into SPICE Engine

SPICE (Super-fast, Parallel, In-memory Calculation Engine) is QuickSight's cache memory. Loading data into SPICE speeds up chart response times and reduces the cost of scanning data directly on S3 through Athena.

1. Return to the QuickSight homepage, select the **Datasets** tab (left menu) -> Click **New dataset**.
2. Select Data Source: **Athena**.
3. Enter the data source name: `YoutubeSentiment_Source` -> Click **Create data source**.
4. In the schema selection panel:
   - **Catalog:** `AwsDataCatalog`
   - **Database:** `sentiment_db`
   - **Table:** `youtube_comments`
   - Click **Select**.
5. Select **Import to SPICE for quicker analytics** -> Click **Visualize**.

---

### Step 5: Build BI Dashboard

On the Analysis screen, set up the core charts (Visuals) to monitor data quality:

1. **Sentiment Distribution Overview (Pie Chart):**
   - *Purpose:* Shows the percentage of opinion streams (Positive, Negative, Neutral).
   - *Configuration:* Drag the `sentiment` field to **Group/Color**. Drag the `comment_id` field to **Value** (applies Count function by default).
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-1.png)

2. **Data Verification Table:**
   - *Purpose:* Lists text details to verify the accuracy of the Claude 3.5 model.
   - *Configuration:* Drag and drop the `vietnamese_text`, `sentiment`, `author`, `published_at`, `original_text`, `language` columns to **Group by**.
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-3.png)

3. **Language Classification (Donut Chart):**
   - *Purpose:* Monitors the language diversity of the raw dataset scraped from YouTube.
   - *Configuration:* Drag `language` to **Group/Color**, `video_id` to **Value**.
![Dashboard](/aws-project/images/youtube/4-Xu-ly-AI/Quicksight-Dashboard-4.png)

---

### Project Summary

At this point, the entire lifecycle of the Serverless Data Pipeline system is complete. The infrastructure is built in strict adherence to modern data engineering principles:
- **Decoupled Architecture:** Uses SQS to isolate risk between the collection layer and processing layer.
- **Cost Optimization:** Applies Chunking and Prompt Engineering to minimize LLM tokens; uses SPICE and Schema-on-read instead of expensive Data Warehouses.
- **Scalability:** Lambda, S3, and Athena automatically scale with input JSON file volume without infrastructure intervention.

The system is production-ready to automatically process thousands of comments per day at near-zero cost within the AWS Free Tier.