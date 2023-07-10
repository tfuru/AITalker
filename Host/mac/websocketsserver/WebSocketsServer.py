import asyncio
from websockets.server import serve

import logging

# コンソールからの接続テスト
# websocat ws://localhost:8765
# history0
# 座る
# こんにちは

class WebSocketsServer:
    def __init__(self, app):
        self.app = app

    async def onmessage(self, websocket):
        async for message in websocket:
            inp = (message).strip()
            logging.debug(f'onmessage {inp}')
            if inp in self.app.EMOTIONS:
                self.app.send_emotion(inp)
            else:
                self.app.send_text(inp)

    async def run(self):
        async with serve(self.onmessage, 
                         "localhost", 8766, 
                         ping_interval=None,
                         ping_timeout=None,
                         open_timeout=None, 
                         close_timeout=None):
            await asyncio.Future()