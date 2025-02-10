import json

def load_config(config_path="config.json"):
    """
    從統一的 JSON 設定檔中讀取配置，並回傳一個字典。
    
    設定檔內容範例：
    {
        "client_id": "你的ClientID",
        "client_secret": "你的ClientSecret",
        "access_token": "你的AccessToken",
        "refresh_token": "你的RefreshToken"
    }
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"讀取設定檔 {config_path} 時發生錯誤: {e}")
        return None
