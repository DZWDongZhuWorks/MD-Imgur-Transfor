import re
import os
import json
import pyimgur
import utils

# 讀取 config.json 取得設定參數
config = utils.load_config("config.json")
if not config:
    print("設定檔讀取失敗，請確認 config.json 存在且格式正確")
    exit(1)

CLIENT_ID = config.get("client_id")
print(f"使用 Imgur API，CLIENT_ID: {CLIENT_ID}")
im = pyimgur.Imgur(CLIENT_ID)

def upload_image(image_path, title):
    """
    上傳圖片，並以參數 title 作為圖片標題
    """
    try:
        uploaded_image = im.upload_image(image_path, title=title)
        print(uploaded_image)
        return uploaded_image
    except Exception as e:
        print(f"上傳失敗 {image_path}: {e}")
        return None

def replace_images_in_md(md_path, record_json="upload_record.json"):
    # 讀取 Markdown 檔案內容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 取得 Markdown 檔案所在目錄
    md_dir = os.path.dirname(md_path)
    # 自動生成記錄檔檔名，例如: 原本檔名為 "example.md"，則記錄檔為 "example_Imgur.json"
    record_json = os.path.basename(md_path).replace(".md", "_Imgur.json")
    
    # 利用正規表達式捕捉 Markdown 圖片的 alt 文字與圖片路徑
    # 此處假設圖片路徑皆位於 assets 目錄下
    pattern = r'!\[(.*?)\]\((assets/.*?)\)'
    # matches 為 [(圖像標題, 圖片路徑), ...]
    matches = re.findall(pattern, content)

    # 用來存放上傳資訊的列表，每筆記錄皆為一個 dict
    records = []

    for alt_text, image_path in matches:
        # 取得圖片檔案的完整路徑
        full_image_path = os.path.join(md_dir, image_path)
        if os.path.exists(full_image_path):
            print(f"上傳圖片: {full_image_path}，標題: {alt_text}")
            uploaded_image = upload_image(full_image_path, title=alt_text)
            if uploaded_image:
                img_url = uploaded_image.link
                # 若上傳成功，取得 deletehash (匿名上傳時會回傳 deletehash)
                deletehash = getattr(uploaded_image, "deletehash", None)
                # 記錄上傳資訊
                record = {
                    "local_path": image_path,              # Markdown 中使用的相對路徑
                    "full_image_path": full_image_path,      # 檔案系統上的完整路徑
                    "img_url": img_url,
                    "deletehash": deletehash,
                    "id": getattr(uploaded_image, "id", None),
                    "title": alt_text                        # 儲存圖片標題
                }
                records.append(record)
                # 將 Markdown 中的本機圖片路徑替換成上傳後的 Imgur URL
                content = content.replace(f"({image_path})", f"({img_url})")
        else:
            print(f"找不到檔案: {full_image_path}")

    # 將更新後的 Markdown 內容寫回檔案
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Markdown 更新完成！")

    # 將上傳記錄寫入 JSON 檔案，存放於 Markdown 同一目錄下
    record_path = os.path.join(md_dir, record_json)
    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    print(f"上傳記錄已保存於 {record_path}")

if __name__ == '__main__':
    md_file = input("請輸入 Markdown 檔案的完整路徑：")
    replace_images_in_md(md_file)
