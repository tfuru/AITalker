# 音声 to テキストの インターフェースクラス
from abc import ABCMeta, abstractmethod

class ISpeechToText(metaclass=ABCMeta):
    @abstractmethod
    def rec_to_text(self, duration):
        pass
        # raise NotImplementedError()