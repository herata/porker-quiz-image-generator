import re
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

def generate_filename(img_url):
    """
    画像URLから指定形式のファイル名を生成
    例: https://.../card_spade_01.png → 01_spade.png
    """
    # ファイル名部分を抽出
    original_name = unquote(img_url.split('/')[-1])
    
    # 正規表現でスートと番号を抽出
    match = re.search(r'card_([a-z]+)_(\d+)\.png', original_name, re.IGNORECASE)
    if match:
        suit = match.group(1)  # spade
        number = match.group(2).zfill(2)  # 01
        return f"{number}_{suit}.png"
    return original_name  # マッチしない場合は元のファイル名

def download_irasutoya_cards(url, output_dir="img//cards"):
    os.makedirs(output_dir, exist_ok=True)

    # HTML取得と解析
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 画像リンク抽出（修正済みセレクタ）
    image_links = []
    entry_content = soup.find('div', {'class': 'entry'})
    for separator in entry_content.find_all('div', {'class': 'separator'}):
        for a_tag in separator.find_all('a', href=True):
            if a_tag.find('img'):
                img_url = a_tag['href']
                # 高解像度URLに変換
                original_url = img_url.replace('/s200/', '/s800/')
                image_links.append(original_url)

    # ダウンロード実行
    for idx, img_url in enumerate(image_links, 1):
        try:
            filename = generate_filename(img_url)
            save_path = os.path.join(output_dir, filename)
            
            # 重複回避処理
            if os.path.exists(save_path):
                base, ext = os.path.splitext(filename)
                filename = f"{base}_{idx}{ext}"
                save_path = os.path.join(output_dir, filename)

            response = requests.get(img_url)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"ダウンロード成功 ({idx}/{len(image_links)}): {filename}")
            time.sleep(1)

        except Exception as e:
            print(f"エラー ({idx}/{len(image_links)}): {str(e)}")
            continue

if __name__ == "__main__":
    marks = ["spade", "heart", "diamond", "club"]
    
    # カード画像のダウンロード
    for mark in marks:
        target_url = f"https://www.irasutoya.com/2010/05/numbercard{mark}.html"
        download_irasutoya_cards(target_url)
    for mark in marks:
        target_url = f"https://www.irasutoya.com/2017/05/facecard{mark}.html"
        download_irasutoya_cards(target_url)
