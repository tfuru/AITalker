# ChatApi クラス
# チャットのメッセージを管理するクラス

import os
import time
import logging
import re

from flask import request
from flask_restful import Resource

from speechtotext.GoogleSpeechToText import GoogleSpeechToText as SpeechToText
from texttospeech.TextToSpeech import TextToSpeech
from ai.AI import AI
from websocketsclient.WebSocketsClient import WebSocketsClient
from sentiment.Sentiment import Sentiment

# 環境変数の取得
# GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
VOICEVOX_ENDPOINT = os.environ['VOICEVOX_ENDPOINT']
VOICEVOX_SPEAKER_ID = int(os.environ['VOICEVOX_SPEAKER_ID'])

# 録音時間
REC_TO_TEXT_DURATION=5

speechToText = SpeechToText()
textToSpeech = TextToSpeech(endpoint=VOICEVOX_ENDPOINT)
ai = AI()
webSocketsClient = WebSocketsClient()
sentiment = Sentiment()

class ChatApi(Resource):
    # OpenAIに問い合わせて回答をもらう
    def answer_to_speech(self, text):
        answer=ai.request(text)
        textToSpeech.text_to_speech(answer, VOICEVOX_SPEAKER_ID)
        return {'status': 'OK', 'text': text, 'answer': answer}
    
    def get(self):
        logging.debug(f'get {request}')
        query=request.args
        if 'text' not in query:
            return {'status': 'NG', 'text':'text is not found'}        
        text = query['text']
        return self.answer_to_speech(text)
    
    def post(self):
        logging.debug(f'post {request}')
        text = request.json["text"]
        return self.answer_to_speech(text)

    def answer_callback(self, answer):
        answer = answer.strip()
        if answer == '':
            return
        logging.info(f'answer_callback {answer}')
        textToSpeech.text_to_speech(answer, VOICEVOX_SPEAKER_ID)
        # answer を websocket で送信
        webSocketsClient.send_text(answer)        
        time.sleep(0.5)

    def start(self):
        logging.info(f'run start')
        textToSpeech.text_to_speech('対話を開始します', VOICEVOX_SPEAKER_ID)
        self.isActive = True
        while self.isActive:
            # 音声認識
            text = speechToText.rec_to_text(REC_TO_TEXT_DURATION)
            if not text:
                continue
            # AIに問い合わせ回答をもらう
            answer=ai.request(text, self.answer_callback)
            logging.info(f'answer {answer}')
            if answer == '':
                continue
            # answer の感情に合わせて websocketsclient にエモーションを送信
            def callback(req):
                if 'emotion' in req:
                    webSocketsClient.send_emotion(req['emotion'])
            sentiment.request(answer, callback)
            
        logging.info(f'run stop')
        textToSpeech.text_to_speech('対話を終了しました', VOICEVOX_SPEAKER_ID)
        webSocketsClient.stop()
        sentiment.stop()

    def stop(self):
        self.isActive = False