# コマンドライン引数で モードを受け取って サウンドの入出力ソースを切り替える

# 確認方法
# PulseAudio を起動
# pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1
# デフォルトの入力ソース
# pacmd list-sources | grep -e 'index:' -e device.string -e 'name:'
# # デフォルトの出力ソース
# pacmd list-sinks | grep -e 'name:' -e 'index:' -e device.string -e 'name:'

import sys
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

args = sys.argv
if len(args) != 2:
    logging.error("Invalid arguments")
    sys.exit(1)

sw = args[1]
sources = {
    "0": ["Channel_1", "1__2", "MacBook Airのマイク, MacBook Airのスピーカー"],
    "1": ["Channel_1__Channel_2.2", "Channel_1__Channel_2.3", "BlackHole 2ch, VB-Cable"],
}
source = sources.get(sw)
if source is None:
    logging.error("Invalid mode")
    sys.exit(1)

logging.info(f"{source[2]}")
subprocess.call(["pactl", "set-default-source", source[0]])
subprocess.call(["pactl", "set-default-sink", source[1]])