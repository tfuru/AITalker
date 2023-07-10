import json as JSON
import requests
import logging
import wave
import subprocess
import re

# 参考 PythonからVOICEVOXを使う
# https://qiita.com/hatt_takumi/items/d65c243294f250724c19

class AudioQuery():
    def __init__(self, endpoint):
        if endpoint is None:
            endpoint = "http://voicevox:50021"
        self.WAV_FILE_PATH = '/tmp/output.wav'
        self.API_AUDIO_QUERY = f"{endpoint}/audio_query"
        self.API_SYNTHESIS = f"{endpoint}/synthesis"

    def audio_query(self, text, speaker):
        params = {"text": text, "speaker": speaker}
        audio_query_resp = requests.post(
            self.API_AUDIO_QUERY,
            params=params)
        logging.debug(f'audio_query_resp: {audio_query_resp.json()}')
        return audio_query_resp
    
    def synthesis(self, speaker, audio_query_resp):
        params = {"speaker": speaker}
        headers = {'Content-Type': 'application/json'}
        synthesis_resp = requests.post(
            self.API_SYNTHESIS,
            headers=headers,
            params=params,
            data=JSON.dumps(audio_query_resp.json())
        )
        logging.debug(f'synthesis_resp: {synthesis_resp.headers}')

        return synthesis_resp
    
    # WAVファイルを保存
    def create_wave(self, synthesis_resp):
        wf = wave.open(self.WAV_FILE_PATH, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(synthesis_resp.content)
        wf.close()            

        return self.WAV_FILE_PATH
    
    # WAVファイルを再生
    def play(self, wav_file_path):
        popen=subprocess.Popen(['aplay', wav_file_path])
        popen.wait()

class TextToSpeech():
    def __init__(self, endpoint = None):
        self.AudioQuery = AudioQuery(endpoint)

    def text_to_speech(self, text, speaker=8):
        # text を !,,, で区切って配列に入れる
        words = re.split('[\n!,。、！？]', text)
        logging.info(f'words: {words}')
        for word in words:
            if word == '':
                continue
            # voicevox への問い合わせ
            audio_query_resp = self.AudioQuery.audio_query(word, speaker)
            synthesis_resp = self.AudioQuery.synthesis(speaker, audio_query_resp)
            wav_file_path = self.AudioQuery.create_wave(synthesis_resp)
            # WAV 音声再生
            self.AudioQuery.play(wav_file_path)

