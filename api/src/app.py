import threading
import json as JSON

import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask_cors import CORS

from chatapi.ChatApi import ChatApi
chatApi=ChatApi()
chatApiThread = threading.Thread(target=chatApi.start)

app = Flask(__name__)
CORS(app)
api = Api(app)

# JSON レスポンスの日本語文字化け対策
@api.representation('application/json')
def output_json(data, code, headers):
    resp = make_response(JSON.dumps(data, ensure_ascii=False), code)
    resp.headers.extend(headers)
    return resp

api.add_resource(ChatApi, '/message')

@app.route("/start")
def start():
    # 音声認識開始
    chatApiThread.start()
    return jsonify({"status": "OK", 'command': 'start'})

@app.route("/stop")
def stop():
    # 音声認識開始
    chatApi.stop()
    try:
        chatApiThread.join()
    except RuntimeError:
        pass
    return jsonify({"status": "OK", 'command': 'stop'})

@app.route("/")
def index():
    return jsonify({"status": "OK", "name": "AITalker v0.0.1"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)