---
title: "2.1 Tạo YouTube API Key"
date: 2026-02-25
weight: 1
---

Để cào được comment, chúng ta cần xin phép Google.

1.  Truy cập **Google Cloud Console**.
   ![Trang chủ Google Cloud Console](/images/2-Chuan-bi/GoogleCloudConsole.png)
2.  Vào **APIs & Services** > **Library** > Tìm và bật **YouTube Data API v3**.
   ![](/images/2-Chuan-bi/APIService.png)
   ![](/images/2-Chuan-bi/APIService.png)
   Tìm  `Youtube data API v3`
   ![](/images/2-Chuan-bi/Find.png)
   ![](/images/2-Chuan-bi/YouTubeAPI.png)
   ![](/images/2-Chuan-bi/Enable.png)
3.  Vào **Credentials** > **Create Credentials** > **API Key**.
   ![](/images/2-Chuan-bi/Credential.png)
   Đặt tên cho API key `YoutubeAPI Key`
   ![](/images/2-Chuan-bi/NameAPI.png)
   Phải restrictions key vì nếu hacker hoặc bot vô tình trộm được Key của bạn, chúng cũng không thể dùng Key này để gọi các dịch vụ tốn tiền khác của Google(như Google Maps, Google Translate,...).
   ![](/images/2-Chuan-bi/restric.png) 
   ![](/images/2-Chuan-bi/APIKey.png) 


> **Lưu ý:** Copy API Key này và lưu lại để dùng cho bước sau.