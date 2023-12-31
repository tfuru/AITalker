# AITalker
メタバース系 AI対話エージェント を作成するためのフレームワークです。

# PulseAudio
Macホストとコンテナ内のオーディオを繋ぐためのソフトウェア  
PulseAudioを起動した状態でDockerコンテナーを起動すると接続される   
```
# PulseAudio を設定
brew install pulseaudio

# PulseAudio を起動
pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1

# PulseAudio 起動確認
pulseaudio --check -v

# PulseAudio を停止
pulseaudio --kill

# pulseaudio デフォルトデバイスの確認
# https://wiki.archlinux.jp/index.php/PulseAudio/%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB#.E3.83.87.E3.83.95.E3.82.A9.E3.83.AB.E3.83.88.E3.81.AE.E5.85.A5.E5.8A.9B.E3.82.BD.E3.83.BC.E3.82.B9.E3.82.92.E8.A8.AD.E5.AE.9A
# http://kamae-norihiro.blogspot.com/2015/09/pulseaudio.html
# デフォルトの入力ソース確認
pacmd list-sources | grep -e 'index:' -e device.string -e 'name:'
pactl set-default-source Channel_1 # MacBook Airのマイク

# デフォルトの出力ソース
pacmd list-sinks | grep -e 'name:' -e 'index:' -e device.string -e 'name:'
pactl set-default-sink 1__2 # MacBook Airのスピーカー
```

# .env 環境変数ファイル
```
cp .env.sample .env
vi .env
```

```
# GOOGLE
GOOGLE_CSE_ID="XXXXX"
GOOGLE_API_KEY="xxxxxxxx"
GOOGLE_APPLICATION_CREDENTIALS=/api/google_application_credentials.json

# OPENAI
OPENAI_API_KEY="sk-XXXXXXX"

# VOICEVOX
VOICEVOX_ENDPOINT="http://voicevox:50021"
VOICEVOX_SPEAKER_ID=8
```

# Docker 環境

`docker-compose.yml` に 記載されているサービスについて説明します。
voicevox
- Voicevox Core 音声合成エンジン
api
- APIサーバー


# Docker 起動手順
```
docker compose build
docker compose up -d

docker compose exec api /bin/bash
```

# HOST側の設定
ホスト側のマウスとキーボードをコンテナ内から操作するためのスクリプト

```
# 必要ライブラリをインストール
pip install --upgrade pip
pip install -r requirements.txt

```