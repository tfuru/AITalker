import pywinctl as pwc
import pyautogui
import pyperclip

import logging

# Clusterを操作するクラス
class ClusterApp:
    def __init__(self):
        self.ws = None
        # エモーションの座標リスト
        self.EMOTIONS = {
            # 履歴
            'history0':[680,175],
            'history1':[750,175],
            'history2':[680,240],
            'history3':[750,240],
            # すべて
            '座る':[680,350],
            'うたたね':[750,350],
            'うたた寝':[750,350],
            'わらう':[680,420],
            'ハート':[750,420], 
            'びっくり':[680,490],
            'いいね':[750,490],
            'それな':[680,560],
            'パチパチ':[750,560],
            '応援':[680,613],
            'ワイワイ':[750,613],            
        }

    def init_window(self, name):
        ws = pwc.getWindowsWithTitle(name)
        if ws:
            self.ws = ws[0]
            self.ws.activate()
            self.ws.moveTo(0, 0)
            self.ws.resizeTo(800, 600)
        else:
            logging.debug('no window found')

    # ウインドウにテキストを送る
    def send_text(self, text):
        logging.info(f'send_text {text}')
        # 日本語はクリップボードにコピーしてペーストする事で送信できる
        if self.ws is None:
            return
        self.ws.activate()
        pyperclip.copy(text)
        pyautogui.doubleClick(90, 545)       
        pyautogui.hotkey('command', 'v')
        pyautogui.press('enter')

    # エモーションを送る
    def send_emotion(self, name):
        logging.info(f'send_emotion {name}')
        if self.ws is None:
            return
        self.ws.activate()
        emotion = self.EMOTIONS[name]
        if emotion:
            pyautogui.click(emotion[0], emotion[1])
