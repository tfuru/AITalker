# import readline
import asyncio

import logging
logging.basicConfig(level=logging.INFO)

from clusterapp.ClusterApp import ClusterApp
from websocketsserver.WebSocketsServer import WebSocketsServer

app = ClusterApp()
webSocketsServer = WebSocketsServer(app)

def main():
    app.init_window('cluster')
    asyncio.run(webSocketsServer.run())

if __name__ == "__main__":
    main()