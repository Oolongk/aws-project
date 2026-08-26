---
weight: 1
date: 2026-02-25
title: "Create YouTube API Key"
chapter: false
pre: "<b>2.1.2.1. </b>"
---

To scrape comments, we need to request permission from Google.

1. Access **Google Cloud Console**.
   ![Google Cloud Console Homepage](/aws-project/images/youtube/2-Chuan-bi/GoogleCloudConsole.png)
2. Go to **APIs & Services** > **Library** > Search for and enable **YouTube Data API v3**.
   ![](/aws-project/images/youtube/2-Chuan-bi/APIService.png)
   ![](/aws-project/images/youtube/2-Chuan-bi/APIService.png)
   Search for `Youtube data API v3`
   ![](/aws-project/images/youtube/2-Chuan-bi/Find.png)
   ![](/aws-project/images/youtube/2-Chuan-bi/YouTubeAPI.png)
   ![](/aws-project/images/youtube/2-Chuan-bi/Enable.png)
3. Go to **Credentials** > **Create Credentials** > **API Key**.
   ![](/aws-project/images/youtube/2-Chuan-bi/Credential.png)
   Name the API key `YoutubeAPI Key`
   ![](/aws-project/images/youtube/2-Chuan-bi/NameAPI.png)
   You must restrict the key so that even if a hacker or bot steals it, they cannot use it to call other paid Google services (such as Google Maps, Google Translate, etc.).
   ![](/aws-project/images/youtube/2-Chuan-bi/restric.png)
   ![](/aws-project/images/youtube/2-Chuan-bi/APIKey.png)



> **Note:** Copy this API Key and save it for use in the next step.