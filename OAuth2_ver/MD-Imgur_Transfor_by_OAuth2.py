import re
import os
import json
import pyimgur
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

# 使用 OAuth2 參數建立綁定帳號的 Imgur 物件
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

def upload_image(image_path):
    try:
        # 上傳圖片時會自動以帳號綁定，若上傳成功，返回的物件中通常會包含 link 與圖片 id
        uploaded_image = im.upload_image(image_path, title="自動上傳 (Account Bound)")
        return uploaded_image
    except Exception as e:
        print(f"上傳失敗 {image_path}: {e}")
        return None

def replace_images_in_md(md_path, record_json="upload_record.json"):
    # 讀取 Markdown 內容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 取得 Markdown 檔案所在目錄（方便組合完整路徑）
    md_dir = os.path.dirname(md_path)
    # 用正規表達式找出 assets 資料夾內的圖片路徑
    pattern = r'!\[.*?\]\((assets/.*?)\)'
    matches = re.findall(pattern, content)

    records = []
    for image_path in matches:
        full_image_path = os.path.join(md_dir, image_path)
        if os.path.exists(full_image_path):
            print(f"上傳圖片: {full_image_path}")
            uploaded_image = upload_image(full_image_path)
            if uploaded_image:
                img_url = uploaded_image.link
                # 帳號上傳時，部分情況下不會回傳 deletehash，此時可改以圖片 id 進行後續刪除
                deletehash = getattr(uploaded_image, "deletehash", None)
                record = {
                    "local_path": image_path,          # Markdown 中的相對路徑
                    "full_image_path": full_image_path,  # 檔案系統上的完整路徑
                    "img_url": img_url,
                    "deletehash": deletehash,            # 可能為 None
                    "id": getattr(uploaded_image, "id", None)
                }
                records.append(record)
                # 將 Markdown 中的本機圖片路徑替換成上傳後的 Imgur 連結
                content = content.replace(f"({image_path})", f"({img_url})")
        else:
            print(f"找不到檔案: {full_image_path}")

    # 將更新後的 Markdown 寫回檔案
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Markdown 更新完成！")

    # 將上傳記錄存成 JSON（存放於 Markdown 同一目錄下）
    record_path = os.path.join(md_dir, record_json)
    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    print(f"上傳記錄已保存於 {record_path}")

if __name__ == '__main__':
    # 將此處換成您 Markdown 檔案的完整路徑
    md_file = r"D:\[Dataset]\Satellite\doc\鼎漢航拍進度總結.md"
    replace_images_in_md(md_file)
