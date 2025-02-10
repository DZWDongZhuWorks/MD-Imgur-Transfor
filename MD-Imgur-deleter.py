import os
import json
import requests
import utils  # 假設 utils 中已有 load_config() 函數

# 讀取 config.json 取得設定參數
config = utils.load_config("config.json")
if not config:
    print("設定檔讀取失敗，請確認 config.json 存在且格式正確")
    exit(1)

CLIENT_ID = config.get("client_id")

def delete_image(deletehash):
    """
    使用 Imgur API 刪除圖片，傳入 deletehash 後回傳刪除是否成功
    """
    url = f"https://api.imgur.com/3/image/{deletehash}"
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(f"刪除失敗, 回應: {response.text}")
        return False

def delete_images(record_json):
    """
    讀取 JSON 記錄檔，根據每筆記錄中的 deletehash 刪除圖床上的圖片
    """
    with open(record_json, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    for record in records:
        deletehash = record.get("deletehash")
        local_path = record.get("local_path")
        img_url = record.get("img_url")
        if deletehash:
            success = delete_image(deletehash)
            if success:
                print(f"成功刪除圖片: {img_url} (對應本機路徑: {local_path})")
            else:
                print(f"刪除圖片失敗: {img_url} (對應本機路徑: {local_path})")
        else:
            print(f"記錄中沒有 deletehash，無法刪除圖片: {img_url} (對應本機路徑: {local_path})")

def restore_images_in_md(md_path, record_json):
    """
    將 Markdown 檔中已被替換成 imgur 連結的圖片 URL 還原回原本的 local 路徑，
    此功能利用 record_json 中儲存的對應關係進行替換。
    """
    # 讀取 Markdown 內容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 讀取 JSON 記錄檔
    with open(record_json, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # 根據每筆記錄，將 imgur 連結還原回原本 local 的相對路徑
    for record in records:
        local_path = record.get("local_path")
        img_url = record.get("img_url")
        if local_path and img_url:
            content = content.replace(f"({img_url})", f"({local_path})")
    
    # 將還原後的內容寫回 Markdown 檔案
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Markdown 中的圖片 URL 已還原為原本的 local 路徑。")

if __name__ == '__main__':
    # 請依序輸入 JSON 記錄檔與要復原的 Markdown 檔案完整路徑
    record_json_path = input("請輸入 JSON 記錄檔的完整路徑：").strip()
    md_file_path = input("請輸入要復原的 Markdown 檔案完整路徑：").strip()
    
    if os.path.exists(record_json_path):
        # 先刪除圖床上的圖片
        delete_images(record_json_path)
        # 再將 Markdown 中的圖片 URL 還原回原本的 local 路徑
        restore_images_in_md(md_file_path, record_json_path)
    else:
        print(f"找不到 JSON 記錄檔: {record_json_path}")
