# import asyncio
import threading
from websockets.sync.client import connect
import logging

class WebSocketsClient:
    def __init__(self):
        self.ws = connect("ws://host.docker.internal:8766")
        logging.info(f'WebSocketsClient init { self.ws }')
        self.msgs = []
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()

    def run(self):
        self.isActive = True
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
