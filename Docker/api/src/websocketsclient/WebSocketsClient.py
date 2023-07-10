import time
import threading
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosedError
import logging

class WebSocketsClient:
    def __init__(self):
        self.WS_URI = "ws://host.docker.internal:8766"        
        logging.info(f'WebSocketsClient init')
        self.msgs = []
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()

    def run(self):
        self.isActive = True
        self.ws = connect(self.WS_URI, open_timeout=None, close_timeout=None)
        while self.isActive:
            if self.msgs == []:
                continue
            msg = self.msgs.pop(0)
            logging.info(f'msg: {msg}')
            self.ws.send(msg)
        self.ws.close()

    def stop(self):
        self.isActive = False

    def send(self, msg):
        logging.info(f'send {msg}')
        self.ws.send(msg)

    def send_emotion(self, emotion):
        self.msgs.append(emotion)
    
    def send_text(self, text):
        self.msgs.append(text)
