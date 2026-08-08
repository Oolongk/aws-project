---
weight: 3
date: 2026-03-05
title: "Build Data Lake with Amazon S3"
chapter: false
pre: "<b>2.1.2.3. </b>"
---

Following the standard Data Engineer architecture, we will build a central Data Lake using **Amazon S3**. Instead of creating multiple separate Buckets, we will use **a single Bucket** and divide it into folders following a multi-tier data management model.

---

### Step 1: Create the S3 Bucket

*Note: Bucket names on AWS must be globally unique.*

1. Log in to the AWS Console and access **Amazon S3**.
2. Click the orange **Create bucket** button.
3. **Bucket name:** Enter a name following the pattern `social-sentiment-datalake-yourname` (Replace *yourname* with your name or student ID).
4. Keep all default settings (especially the *Block all public access* feature).
5. Scroll to the bottom and click **Create bucket**.
![S3 folder structure](/aws-project/images/youtube/2-Chuan-bi/S3-1.png)
![S3 folder structure](/aws-project/images/youtube/2-Chuan-bi/S3-2.png)

### Step 2: Create Folders (Data Layers)

Click into the newly created Bucket, then click **Create folder** to create the following 3 folders in sequence:

1. **`raw_data`**: Storage zone for raw data (Bronze Layer) scraped directly from YouTube by the Ingestor function.
2. **`processed_data`**: Storage zone for cleaned data with AI-labeled sentiment (Silver Layer).
3. **`athena_results`**: A required technical folder for storing log files every time AWS Athena runs a query.

![S3 folder structure](/aws-project/images/youtube/2-Chuan-bi/S3-3.png)