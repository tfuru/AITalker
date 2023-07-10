# import asyncio
from websockets.sync.client import connect
import logging

class WebSocketsClient:
    def __init__(self):
        self.ws = connect("ws://host.docker.internal:8766")
        logging.info(f'WebSocketsClient init { self.ws }')

    def close(self):
        self.ws.close()

    def send(self, msg):
        logging.info(f'send {msg}')
        self.ws.send(msg)

    def send_emotion(self, emotion):
        self.send(emotion)
    
    def send_text(self, text):
        self.send(text)