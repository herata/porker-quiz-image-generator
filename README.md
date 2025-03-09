# porker-quiz-image-generator

## 概要

ポーカークイズ（麻雀の何切る問題のような）向けの画像生成ツールです。ポーカーテーブルの状況を可視化し、問題形式の画像を生成できます。

`python 3.13.0`で構築しており、バージョン管理は[mise](https://mise.jdx.dev/)を使用しています。

## セットアップ

### パッケージインストール

```bash
pip install -r requirements.txt
```

### カード画像の準備

トランプ画像はいらすとやのものを利用しています。自前で準備したカード画像を使用する場合は、`img/cards`配下に以下の要領でカード画像を格納してください。裏向きのカード画像も`card_back.png`として格納する必要があります。

```
/Users/suguru/dev/porker-quiz-image-generator
|--.gitignore
|--.mise.toml
|--README.md
|--download.py
|--img
|  |--cards
|  |  |--01_club.png    # クラブのエース
|  |  |--01_diamond.png # ダイヤのエース
|  |  |--01_heart.png   # ハートのエース
|  |  |--01_spade.png   # スペードのエース
|  |  |--02_club.png    # クラブの2
|  |  |--...
|  |  |--13_heart.png   # ハートのキング
|  |  |--13_club.png    # クラブのキング
|  |  |--card_back.png  # カードの裏面
|  |--table
|  |  |--table.png
|--main.py
```

いらすとやからカード画像をダウンロードする場合は以下のスクリプトを実行してください：

```bash
python download.py
```

※カードの裏面画像はいらすとやのページから手動でダウンロードしてください。

ダウンロード後、以下のコマンドで画像サイズをテーブルに合わせてリサイズしてください：

```bash
python resize.py
```

### ポーカーシナリオの生成

`main.py`内のゲーム状態を編集することで、希望のシナリオを設定できます。ゲーム状態の形式は以下の通りです：

```python
game_state = {
    'hero': {
        'position': 'btn',     # ヒーローのポジション（sb, bb, utg, hj, co, btn）
        'cards': ['As', 'Kd'], # ヒーローのホールカード
        'bet': 30             # ヒーローのベット額
    },
    'villains': {
        'sb': {'bet': 3},     # 各ポジションのベット額
        'bb': {'bet': 10},    # プレイヤーがいない場合はNone
        'utg': {'bet': 15},
        'hj': {'bet': 25},
        'co': None
    },
    'board': ['Th', 'Jc', 'Qd', '9c', 'Ac'], # コミュニティカード（0〜5枚）
    'pot': 30                 # ポットサイズ
}
```

カードの表記方法：
- ランク：A（エース）, 2-9, T（10）, J（ジャック）, Q（クイーン）, K（キング）
- スート：h（ハート）, d（ダイヤ）, s（スペード）, c（クラブ）
例：'As'（スペードのエース）, 'Th'（ハートの10）

画像を生成するには以下のコマンドを実行します：

```bash
python main.py
```

生成された画像は`poker_table_output.png`として保存されます。
