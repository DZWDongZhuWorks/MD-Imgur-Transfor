# 透過Imgur帳號進行上傳

## Usage

1. 註冊 [API](https://api.imgur.com/oauth2/addclient)
2. 修改 [獲取token](Imgur_get_tokens_by_pin.py)中的 `client_id` 與 `client_secret`
3. 執行程式碼
4. 程式碼會回傳認證URL連結，複製於瀏覽器中並開啟，請確認並取得PIN碼
5. 將PIN碼回傳至程式碼中，程式碼會自動取得token

## TODO

[主程式](MD-Imgur_Transfor_by_OAuth2.py)尚未完工
