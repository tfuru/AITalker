import sys
import time
import logging
logging.basicConfig(level=logging.INFO)

from WebSocketsClient import WebSocketsClient

webSocketsClient = WebSocketsClient()
webSocketsClient.send_emotion("ハート")
webSocketsClient.send_emotion("ワイワイ")
time.sleep(1)
webSocketsClient.send_text("こんにちは AIももです")
webSocketsClient.send_text("こんばんわ AIももです")
webSocketsClient.stop()
sys.exit(0)