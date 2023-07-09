# Google 音声 to テキストの インターフェースクラス
import io
import logging

import subprocess
from speechtotext.ISpeechToText import ISpeechToText

from google.cloud import speech

# 録音
# http://vimvimvim.blogspot.com/2012/10/aplay-arecord.html
# arecord -c 1 -t wav -r 8000 -f S16_LE -d 3 /tmp/input.wav
# aplay /tmp/input.wav 

# 参考
# https://tech-blog.optim.co.jp/entry/2020/02/21/163000#%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%BD%A2%E5%BC%8F%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AA%E3%83%B3%E3%82%B0%E5%91%A8%E6%B3%A2%E6%95%B0%E3%82%92%E6%AF%94%E8%BC%83%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B

class GoogleSpeechToText(ISpeechToText):
    def __init__(self):
        logging.debug(f'GoogleSpeechToText')
        self.path = '/tmp/input.wav'
        self.encode='wav'
        self.sample_rate=8000
        self.audio_channel = 1
        self.ENCODE={
            'flac': speech.RecognitionConfig.AudioEncoding.FLAC,
            'wav':  speech.RecognitionConfig.AudioEncoding.LINEAR16,
            'ogg':  speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            'amr':  speech.RecognitionConfig.AudioEncoding.AMR,
            'awb':  speech.RecognitionConfig.AudioEncoding.AMR_WB
        }
        self.language_code = 'ja-JP'
        self.client = speech.SpeechClient()

    # 録音して音声認識する duration は録音時間
    def rec_to_text(self, duration):        
        logging.info(f'rec_to_text')
        # 録音する
        arecord_cmd=f'arecord -c {self.audio_channel} -t {self.encode} -r {self.sample_rate} -f S16_LE -d {duration} {self.path}'
        logging.debug(f'arecord_cmd: {arecord_cmd}')
        arecord_result = subprocess.run(arecord_cmd, shell=True, check=True)
        logging.debug(f'arecord_result: {arecord_result}')

        # path の音声ファイルを読み込む
        with io.open(self.path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=self.ENCODE[self.encode],
            sample_rate_hertz=self.sample_rate,
            language_code=self.language_code,
            audio_channel_count=1,
            enable_separate_recognition_per_channel=True)
        response = self.client.recognize(config=config, audio=audio)

        result = ''
        for r in response.results:
            # logging.debug('Transcript: {}'.format(r.alternatives[0].transcript))
            result += f'{r.alternatives[0].transcript} '
        if result == '':
            return ''
        result = result.strip()
        logging.info(f'rec_to_text result {result}')
        return result
