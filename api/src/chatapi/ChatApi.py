# ChatApi クラス
# チャットのメッセージを管理するクラス

import os
import time
import logging

from flask import request
from flask_restful import Resource

from speechtotext.GoogleSpeechToText import GoogleSpeechToText as SpeechToText
from texttospeech.TextToSpeech import TextToSpeech
from ai.AI import AI

# 環境変数の取得
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
VOICEVOX_ENDPOINT = os.environ['VOICEVOX_ENDPOINT']
VOICEVOX_SPEAKER_ID = int(os.environ['VOICEVOX_SPEAKER_ID'])

speechToText = SpeechToText()
textToSpeech = TextToSpeech(endpoint=VOICEVOX_ENDPOINT)
ai = AI()

class ChatApi(Resource):
    # OpenAIに問い合わせて回答をもらう
    def answer(self, text):
        answer=ai.request(text)
        textToSpeech.text_to_speech(answer, VOICEVOX_SPEAKER_ID)
        return {'status': 'OK', 'text': text, 'answer': answer}
    
    def get(self):
        logging.debug(f'get {request}')
        query=request.args
        if 'text' not in query:
            return {'status': 'NG', 'text':'text is not found'}        
        text = query['text']
        return self.answer(text)
    
    def post(self):
        logging.debug(f'post {request}')
        text = request.json["text"]
        return self.answer(text)

    def start(self):
        logging.info(f'run start')
        textToSpeech.text_to_speech('対話を開始します', VOICEVOX_SPEAKER_ID)
        self.isActive = True
        while self.isActive:
            # 音声認識
            text = speechToText.rec_to_text(3)
            if not text:
                continue
            # AIに問い合わせ回答をもらう
            answer=ai.request(text)
            # 回答を音声合成
            textToSpeech.text_to_speech(answer, VOICEVOX_SPEAKER_ID)
            time.sleep(0.5)
        logging.info(f'run stop')
        textToSpeech.text_to_speech('対話を終了しました', VOICEVOX_SPEAKER_ID)

    def stop(self):
        self.isActive = False