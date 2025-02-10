import requests
import utils

config = utils.load_config("config.json")
if not config:
    print("設定檔讀取失敗，請確認 config.json 存在且格式正確")
    exit(1)
    
client_id = config.get("client_id")
print(f"使用 Imgur API，CLIENT_ID: {client_id}")

headers = {"Authorization": f"Client-ID {client_id}"}
url = "https://api.imgur.com/3/image"
with open(r"c:\Users\Rontgen-W11-NB\Downloads\SAM_crop_output.png", "rb") as f:
    data = {"image": f.read()}
response = requests.post(url, headers=headers, data=data)
print("HTTP 狀態碼:", response.status_code)
print("回傳內容:", response.text)
