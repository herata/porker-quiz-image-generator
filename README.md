# porker-quiz-image-generator

## 概要

ポーカークイズ（麻雀何切る問題のような）向けの画像ジェネレーターです。

`python 3.13.0`で構築しており、バージョン管理は個人的に[mise](https://mise.jdx.dev/)を使用しています。

## 手順

### パッケージインストール

```bash
pip install -r requiments.txt
```

### トランプ画像準備

トランプ画像はいらすとやのものを利用しています。
自前で準備したカード画像を使用する場合は、`img/cards`配下に以下の要領でカード画像を格納してください。裏向きのカード画像も`card_back.png`として格納してください。

```
/Users/suguru/dev/porker-quiz-image-generator
|--.gitignore
|--.mise.toml
|--README.md
|--download.py
|--img
|  |--cards
|  |  |--01_club.png
|  |  |--01_diamond.png
|  |  |--01_heart.png
|  |  |--01_spade.png
|  |  |--02_club.png
|  |  |--...
|  |  |--13_heart.png
|  |  |--13_club.png
|  |  |--card_back.png
|  |--table
|  |  |--table.png
|--main.py
```

いらすとやからダウンロードする場合は以下スクリプトを実行し、ダウンロードしてください。（裏向きカードがいらすとやのページから手動でお願いします）

```bash
python download.py
```

次に以下より画像のサイズを変更してください。

```bash
python resize.py
```

### スポット画像生成

`main.py`の以下のあたりで生成したいスポットの情報を設定してください。

```python
...
# 使用例
if __name__ == "__main__":
    # 入力パラメータ
    hero_position = "hj"  # ヒーローのポジション
    hero_cards = ["As", "Kd"]  # ヒーローの手札
    board_cards = ["Th", "Jc", "Qd", "9c"]  # ボードのカード
    villain_positions = ["co", "btn", "bb"]  # 複数のVillainのポジション
...
```

設定後`main.py`を実行すると`porker_table_output.png`が生成されます。

```bash
python main.py
```
