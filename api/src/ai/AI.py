import os
import logging

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.agents import Tool, initialize_agent
from langchain.utilities import GoogleSearchAPIWrapper

# 参考
# https://note.com/strictlyes/n/n6de1a36a6e7e

class AI:
    def __init__(self):
        # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        temperature=0.0
        # gpt-3.5-turbo-16k
        self.llm=ChatOpenAI(temperature=temperature, model_name='gpt-3.5-turbo')
        
        # プロンプト作成
        system_template="""あなたは音声で対話するAIです。
        小学生にも分かるように簡単に短く会話するようにしてください。
        語尾に必ず にゃん をつけてください。

        以下の過去の会話履歴を参考にして会話をしてください。
        {chat_history}
        """
        human_template="{input}"
        self.prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_template),
                HumanMessagePromptTemplate.from_template(human_template),
            ])
        self.memory=ConversationBufferWindowMemory(
            k=5, # 記憶回数
            memory_key="chat_history",
            human_prefix="User", 
            ai_prefix="Ai",
            input_key="input",
            return_messages=True
            )
        
    def request(self, input):
        # verbose プロンプト途中結果の表示有無
        chain=LLMChain(llm=self.llm, 
                          prompt=self.prompt,
                          memory=self.memory,
                          verbose=False)
        result = chain.run(input=input)
        answer=result.strip()
        return answer
    
    # TODO Agent と Toursを使った会話 だが、現状は想定通りに動作しない
    def request_agent(self, text):
        search = GoogleSearchAPIWrapper()
        tools = [
            Tool(
                name = "Search",
                func=search.run,
                description="Helpful if you need to answer a question"
            )
        ]
        prefix = """Please answer the following questions in Japanese as briefly as possible. You can access the following tools:"""
        suffix = """Don't forget to write your final answer in Japanese. Please be sure to add "nyan" at the end."""
        agent = initialize_agent(
            tools,
            self.llm,
            # agent="chat-zero-shot-react-description",
            agent="chat-conversational-react-description",
            verbose=True,
            memory=self.memory,
            prefix=prefix,
            suffix=suffix)
        
        try:
            result = agent.run(input=text)
        except ValueError as e:
            result = str(e)
            if not result.startswith("Could not parse LLM output: `"):
                raise e
            result = result.removeprefix("Could not parse LLM output: `").removesuffix("`")

        answer=result.strip()
        logging.debug(answer)
        # buffer = self.memory.load_memory_variables({})
        # logging.info(f'memory buffer {buffer}')
        return answer
