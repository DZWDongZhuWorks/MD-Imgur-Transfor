# 自動化 Markdown assets 圖片上傳與URL路徑替換與圖床刪除與路徑復原

## Install

    # python3.10.16
    pip install -r requirements.txt
    

## Usage

1. 註冊 [API](https://api.imgur.com/oauth2/addclient)
2. 獲得 Client ID 並修改 `config.json` 中的 `client_id`
3. 執行程式碼

    python MD-Imgur-Transfor.py

4. 輸入Markdown檔案路徑
5. 程式碼會自動將圖片上傳至Imgur並替換Markdown中的圖片連結
6. 同時產出`upload_record.json`，作為刪除時使用的紀錄

## Delete Imgur Image

刪除Imgur上的圖片，並且將Markdown檔案中的圖片連結還原

1. 執行

    python MD-Imgur-deleter.py

2. 輸入`Imgue.json`路徑
3. 輸入欲還原之md檔案路徑

## Notice

1. 圖片並沒有與Imgur帳號綁定，如果要刪除，只能透過上傳圖片時的deletehash進行刪除，因此務必保留`upload_record.json`，否則無法刪除圖片。
2. 該圖片的隱私設定為擁有連結者皆可查看，並且無有效期限。
3. 官方文件並沒有明說，但Imgur api 每小時似乎有上傳數量限制50張。
