from PIL import Image
import os


def resize_images(folder_path="./img/cards", target_width=100):
    """
    指定されたフォルダ内の全画像ファイルをアスペクト比を保ったまま指定の横幅にリサイズする

    Parameters:
        folder_path (str): 画像ファイルが格納されているフォルダのパス
        target_width (int): リサイズ後の横幅（ピクセル）
    """

    # サポートされている画像形式
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # フォルダ内のファイルを処理
    processed = 0
    skipped = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # ファイルが画像かどうかを確認
        if os.path.isfile(file_path) and any(filename.lower().endswith(fmt) for fmt in supported_formats):
            try:
                # 画像を開く
                img = Image.open(file_path)

                # 元の画像サイズを取得
                original_width, original_height = img.size

                # 新しい高さを計算（アスペクト比を維持）
                new_height = int(original_height * (target_width / original_width))

                # リサイズ
                resized_img = img.resize((target_width, new_height), Image.LANCZOS)

                # 保存
                resized_img.save(file_path)

                processed += 1
                print(f"{filename} ({original_width}x{original_height} → {target_width}x{new_height})")

            except Exception as e:
                print(f"エラー: {filename} の処理中に問題が発生しました - {str(e)}")
                skipped += 1
        else:
            skipped += 1

    print("\nDone!")


if __name__ == "__main__":
    resize_images()
