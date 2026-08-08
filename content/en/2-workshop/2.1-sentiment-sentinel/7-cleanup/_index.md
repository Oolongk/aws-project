---
weight: 7
date: 2026-03-18
title: "Resource Cleanup"
chapter: false
pre: "<b>2.1.7. </b>"
---

Congratulations on completing the project! In the world of Cloud Computing, resources cost money, and if forgotten they will "burn through" your budget. Even though our project primarily uses Serverless services within the Free Tier, cleaning up thoroughly after practice is a mandatory habit for every professional Data Engineer.

Below is the precise cleanup order so you don't miss any "Zombie resources".

---

### Step 1: Unsubscribe from AWS QuickSight (Top Priority)
QuickSight is billed monthly ($24/month), so this is the first thing you must "eliminate".

1. Log in to **AWS QuickSight**.
2. Click the Avatar icon in the top right corner -> Select **Manage QuickSight**.
3. Select **Account settings** in the left menu.
4. Scroll to the bottom and click **Delete account** (or Unsubscribe).
5. Follow the on-screen instructions (usually requires re-entering the account name) to confirm deletion.
*(Note: This action will permanently delete all your Dashboards and Datasets.)*

---

### Step 2: Disable the Amazon EventBridge Alarm
If you don't disable this, the system will automatically wake up tomorrow morning to scrape data and generate new costs.

1. Access the **Amazon EventBridge** service -> Select **Schedules** in the left menu.
2. Find the `Daily-Youtube-Data-Ingestion` schedule you created in Chapter 6.
3. Check it and click **Delete**.

---

### Step 3: Clean Up Amazon S3 Storage (Very Important)
AWS does not allow you to delete a Bucket if it still contains files. You must "empty the trash" before deleting the bucket.

1. Access **Amazon S3** -> Select **Buckets**.
2. Find your Data Lake Bucket (and the Athena results Bucket `athena_results` if applicable).
3. **Empty it:** Check the Bucket -> Click the **Empty** button in the top menu -> Type `permanently delete` to confirm clearing all files inside.
4. **Delete the bucket:** After successfully emptying, check the Bucket again -> Click **Delete** -> Enter the Bucket name to confirm permanent deletion.

---

### Step 4: Delete Database, Queues, and Functions

Access the following services in sequence and click Delete:

1. **Amazon DynamoDB:**
   - Go to **Tables**. Check the `YoutubeCommentsTracker` table -> Click **Delete**.
   - Do the same for the `YoutubeVideoBlacklist` table.
2. **Amazon SQS:**
   - Go to **Queues**. Check `YoutubeVideoQueue` -> Click **Delete**.
3. **AWS Lambda:**
   - Go to **Functions**. Check all 3 functions: `Producer_Lambda`, `Consumer_Lambda`, `Transformer_Lambda`.
   - Click **Actions** -> Select **Delete**.
4. **Amazon Athena (Optional):**
   - The original data on S3 has been deleted so the tables in Athena will also automatically become invalid. You can open the Query Editor and run the command `DROP DATABASE sentiment_db CASCADE;` to clean up the virtual schema.

---

### Step 5: Clean Up IAM Roles (Optional Advanced)
Although IAM doesn't incur costs, deleting unused Roles keeps your account tidy and more secure.

1. Access **AWS IAM** -> Select **Roles**.
2. Find and delete the Roles you created for Lambda (e.g., Roles with access to SQS, DynamoDB, Bedrock).