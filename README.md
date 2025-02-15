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
自前で準備したカード画像を使用する場合は、`img/cards`配下に以下の要領でカード画像を格納してください。

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
|  |--table
|  |  |--table.png
|--main.py
```

いらすとやからダウンロードする場合は以下スクリプトを実行し、ダウンロードしてください。

```bash
python download.py
```