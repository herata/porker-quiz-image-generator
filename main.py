import os
import cv2
import numpy as np


# ポーカーテーブル画像生成クラス
class PokerTableGenerator:

    # カードサイズ（テーブルサイズに合わせて調整）
    CARD_WIDTH = 100
    CARD_HEIGHT = 147

    # ポットサイズの中央座標
    POT_SIZE_COORDS = (512, 495)

    # ポジションの座標マッピング (x, y) - 1024x732のテーブル画像に最適化
    POSITION_COORDS = {
        'sb': (690, 570),   # スモールブラインド
        'bb': (340, 570),   # ビッグブラインド
        'utg': (120, 330),  # アンダーザガン
        'hj': (340, 100),   # ハイジャック
        'co': (690, 100),   # カットオフ
        'btn': (900, 330)   # ボタン
    }

    # ベットの座標マッピング
    BET_COORDS = {
        'sb': (590, 700),   # スモールブラインド
        'bb': (435, 700),   # ビッグブラインド
        'utg': (175, 465),  # アンダーザガン
        'hj': (435, 230),    # ハイジャック
        'co': (590, 230),    # カットオフ
        'btn': (845, 465)   # ボタン
    }

    # コミュニティカードのポジション
    COMMUNITY_COORDS = {
        0: (240, 300),  # 1枚目（フロップ1）
        1: (350, 300),  # 2枚目（フロップ2）
        2: (460, 300),  # 3枚目（フロップ3）
        3: (570, 300),  # 4枚目（ターン）
        4: (680, 300)   # 5枚目（リバー）
    }

    def __init__(self, table_path='img/table/table.png', cards_dir='img/cards'):
        """初期化"""
        self.table_path = table_path
        self.cards_dir = cards_dir

    def load_image(self, path):
        """画像を読み込む"""
        if not os.path.exists(path):
            print(f"警告: 画像ファイルが見つかりません: {path}")
            return None

        try:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"警告: 画像の読み込みに失敗しました: {path}")
                return None

            # アルファチャンネルがない場合は追加
            if len(img.shape) == 3 and img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

            return img
        except Exception as e:
            print(f"画像読み込みエラー ({path}): {str(e)}")
            return None

    def get_card_image(self, card_code):

        if not card_code:
            return None

        # カードコードをファイル名に変換
        rank = card_code[0].upper()
        suit = card_code[1].lower()

        # ランクの変換（10はTとして扱う）
        rank_map = {'2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07', '8': '08', '9': '09', 'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '01'}

        # スートの変換
        suit_map = {'h': 'heart', 's': 'spade', 'd': 'diamond', 'c': 'club'}

        if rank not in rank_map or suit not in suit_map:
            print(f"警告: 無効なカードコード: {card_code}")
            return None

        filename = f"{rank_map[rank]}_{suit_map[suit]}.png"
        card_path = os.path.join(self.cards_dir, filename)

        # カード画像を読み込む
        card_img = self.load_image(card_path)

        return card_img

    def overlay_image(self, background, foreground, x, y):
        """透過画像を背景に合成"""
        if foreground is None:
            return background

        # 画像の範囲
        h, w = foreground.shape[:2]

        # BGRとアルファチャンネルを分離
        alpha = foreground[:, :, 3:4] / 255.0
        fg_bgr = foreground[:, :, :3]

        # ROIを取得
        roi = background[y:y + h, x:x + w].copy()

        # BGRAに変換（必要な場合）
        if len(roi.shape) == 2 or roi.shape[2] == 1:
            roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        if roi.shape[2] == 3:
            # アルファブレンディング（BGRのみ）
            blended = fg_bgr * alpha + roi * (1 - alpha)
            background[y:y + h, x:x + w] = blended.astype(np.uint8)
        else:
            # アルファブレンディング（BGRAの場合）
            blended = fg_bgr * alpha + roi[:, :, :3] * (1 - alpha)
            blended_alpha = alpha + roi[:, :, 3:4] / 255.0 * (1 - alpha)
            result = np.concatenate([blended, blended_alpha * 255], axis=2)
            background[y:y + h, x:x + w] = result.astype(np.uint8)

        return background

    def place_board_cards(self, board_cards):
        """ボードカードを配置"""
        if not board_cards:
            return

        # ボードに表示するカードの最大数
        max_cards = 5
        num_cards = min(len(board_cards), max_cards)

        # カードの配置
        for i, card_code in enumerate(board_cards[:num_cards]):
            card_img = self.get_card_image(card_code)
            if card_img is not None:
                # 座標を取得
                x, y = self.COMMUNITY_COORDS[i]
                self.table_img = self.overlay_image(self.table_img, card_img, x, y)

    def place_cards(self, position, hero_cards=None):
        """プレイヤーの手札をポジションに合わせて配置"""

        # ポジションの座標を取得
        base_x, base_y = self.POSITION_COORDS[position.lower()]

        # 2枚のカードを配置
        total_width = 2 * self.CARD_WIDTH
        start_x = base_x - total_width // 2
        start_y = base_y - self.CARD_HEIGHT // 2

        if hero_cards is None:
            # 裏面カードを配置
            for i in range(2):
                x = start_x + i * (self.CARD_WIDTH)
                y = start_y
                filename = "card_back.png"
                card_path = os.path.join(self.cards_dir, filename)
                card_img = self.load_image(card_path)
                self.table_img = self.overlay_image(self.table_img, card_img, x, y)
        else:
            # プレイヤーの手札を配置
            for i, card_code in enumerate(hero_cards):
                x = start_x + i * (self.CARD_WIDTH)
                y = start_y
                card_img = self.get_card_image(card_code)
                self.table_img = self.overlay_image(self.table_img, card_img, x, y)

    def draw_pot_size(self, pot_size):
        """ポットサイズを表示"""
        text = f"{pot_size}"
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1.0
        thickness = 2
        color = (255, 255, 255, 255)
        thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

        x = self.POT_SIZE_COORDS[0] - text_width // 2
        y = self.POT_SIZE_COORDS[1] + text_height // 2

        org = (x, y)
        cv2.putText(self.table_img, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    def draw_bet_size(self, position, bet_size):
        """ベットサイズを表示"""
        text = f"{bet_size}"
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1.0
        thickness = 2
        color = (255, 255, 255, 255)
        thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

        x, y = self.BET_COORDS[position.lower()]
        x -= text_width // 2
        y += text_height // 2

        org = (x, y)
        cv2.putText(self.table_img, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    # def generate_table_image(self, hero_position, hero_cards, board_cards, villan_positions, pot_size, output_path):
    #     """ポーカーテーブル画像を生成"""
    #     # テーブル画像をリセット
    #     self.table_img = self.load_image(self.table_path)

    #     # ボードカードを配置
    #     self.place_board_cards(board_cards)

    #     # プレイヤーの手札を配置
    #     self.place_cards(hero_position, hero_cards)

    #     # Villainの手札を配置
    #     for position in villan_positions:
    #         self.place_cards(position)

    #     if pot_size:
    #         # ポットサイズを表示
    #         self.draw_pot_size(pot_size)

    #     # 画像を保存
    #     try:
    #         cv2.imwrite(output_path, self.table_img)
    #         print(f"画像を保存しました: {output_path}")
    #     except Exception as e:
    #         print(f"画像保存エラー: {str(e)}")

    #     return self.table_img
    def generate_table_image(self, game_state, output_path):
        """ポーカーテーブル画像を生成"""
        # テーブル画像をリセット
        self.table_img = self.load_image(self.table_path)

        # ボードカードを配置
        self.place_board_cards(game_state['board'])

        # プレイヤーの手札を配置
        self.place_cards(game_state['hero']['position'], game_state['hero']['cards'])

        # Villainの手札を配置
        for position, villain in game_state['villains'].items():
            self.place_cards(position)

        # ベットサイズを表示
        for position, villain in game_state['villains'].items():
            if villain and 'bet' in villain and villain['bet'] is not None:
                self.draw_bet_size(position, villain['bet'])

        # ヒーローのベットサイズを表示
        if 'bet' in game_state['hero'] and game_state['hero']['bet'] is not None:
            self.draw_bet_size(game_state['hero']['position'], game_state['hero']['bet'])

        # ポットサイズを表示
        if game_state['pot']:
            self.draw_pot_size(game_state['pot'])

        # 画像を保存
        try:
            cv2.imwrite(output_path, self.table_img)
            print(f"画像を保存しました: {output_path}")
        except Exception as e:
            print(f"画像保存エラー: {str(e)}")

        return self.table_img


# 使用例
if __name__ == "__main__":
    # 入力パラメータ
    # hero_position = "btn"  # ヒーローのポジション
    # hero_cards = ["As", "Kd"]  # ヒーローの手札
    # board_cards = ["Th", "Jc", "Qd", "9c", "Ac"]  # ボードのカード
    # villain_positions = ["sb", "bb", "utg", "hj", "co"]  # 複数のVillainのポジション
    # pot_size = 100  # ポットサイズ
    game_state = {
        'hero': {
            'position': 'btn',
            'cards': ['As', 'Kd'],
            'bet': 30
        },
        'villains': {
            'sb': {'bet': 3},
            'bb': {'bet': 10},
            'utg': {'bet': 15},
            'hj': {'bet': 25},
            'co': None
        },
        'board': ['Th', 'Jc', 'Qd', '9c', 'Ac'],
        'pot': 30
    }

    # 出力ファイルパス
    output_path = "poker_table_output.png"

    # ポーカーテーブル画像を生成
    generator = PokerTableGenerator()
    # generator.generate_table_image(hero_position, hero_cards, board_cards, villain_positions, pot_size, output_path)
    generator.generate_table_image(game_state, output_path)
