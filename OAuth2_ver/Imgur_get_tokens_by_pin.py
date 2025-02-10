import requests
import utils


config = utils.load_config("config.json")
if not config:
    print("設定檔讀取失敗，請確認 config.json 存在且格式正確")
    exit(1)
    
    
# 請確認config.json是否已正確設定
CLIENT_ID = config.get("client_id")
CLIENT_SECRET = config.get("client_secret")
ACCESS_TOKEN = config.get("access_token")
REFRESH_TOKEN = config.get("refresh_token")

def get_tokens_by_pin():
    # 產生授權 URL，要求使用 PIN 授權方式
    authorization_url = f"https://api.imgur.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=pin"
    print("請開啟下列 URL 並授權應用程式：")
    print(authorization_url)

    # 請使用者將授權後所顯示的 PIN 輸入
    pin = input("請輸入授權後顯示的 PIN：").strip()

    # 使用 PIN 交換 ACCESS_TOKEN 與 REFRESH_TOKEN
    token_url = "https://api.imgur.com/oauth2/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'pin',
        'pin': pin
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        print("取得 Token 成功！")
        print("Access Token :", token_data.get("access_token"))
        print("Refresh Token:", token_data.get("refresh_token"))
        # 您可以將 token_data 存檔以便後續使用
        return token_data
    else:
        print("取得 Token 失敗：", response.text)
        return None

if __name__ == '__main__':
    get_tokens_by_pin()
