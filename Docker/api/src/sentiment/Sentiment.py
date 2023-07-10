import threading
import logging
from transformers import pipeline

# 感情解析
# 参考 
# https://note.com/npaka/n/n1766c894c1f2

# コマンドライン
# python test.py こんにちは
# python test.py 悲しいです

class Sentiment:
    def __init__(self):
        # パイプラインの準備
        self.classifier = pipeline(
                "sentiment-analysis",
                model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
                top_k=None
            )
        self.requests = []
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        logging.info(f'start')
        self.isActive = True
        while self.isActive:
            if self.requests == []:
                continue
            
            req = self.requests.pop(0)
            logging.debug(f"req: {req}")
            if 'callback' not in req:
                continue

            callback = req['callback']
            result = self.classifier(req['text'])
            logging.debug(f"result: {result}")
            if callback == None:
                continue            
            if result == []:
                callback({'status': 'NG'})
                continue

            score = {
                'positive': 0,
                'neutral': 0,
                'negative': 0,
            }
            for re in result[0]:
                # logging.info(f"re: {re}")
                score[re['label']] = round(re['score'], 4) 
            emotion = ''
            if score['positive'] > 0.4:
                emotion = 'ワイワイ'
            if score['neutral'] > 0.4:
                emotion = 'わらう'
            if score['negative'] > 0.4:
                emotion = 'びっくり'
            logging.info(f"emotion: {emotion}")            
            if emotion == '':
                callback({'status': 'NG'})
                continue
            callback({'status': 'OK', 'emotion': emotion, 'score': score})

    def stop(self):
        logging.info(f'stop')
        self.isActive = False

    def request(self, text, callback=None):
        # logging.debug(f"request: {text}")
        if text == '':
            return
        self.requests.append({'text': text, 'callback': callback})
