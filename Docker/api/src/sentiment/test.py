import sys
import time
import logging
from Sentiment import Sentiment

logging.basicConfig(level=logging.DEBUG)

args = sys.argv

if len(args) != 2:
    logging.error("Invalid arguments")
    sys.exit(1)

def callback(req):
    logging.info(f"callback: {req}")

sentiment = Sentiment()
sentiment.request(text=args[1], callback=callback)
sentiment.request(text=args[1], callback=callback)
time.sleep(10)
sentiment.stop()
