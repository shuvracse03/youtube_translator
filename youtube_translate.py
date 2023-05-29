from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import os
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from googletrans import Translator
from langchain.tools import BaseTool
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI

from typing import Optional, Type
from langchain.callbacks.manager import AsyncCallbackManager, CallbackManager



os.environ["OPENAI_API_KEY"] = 'OPENAPI-KEY'

class YoutubeTranslator(BaseTool):
    name = "youtube_translator"
    description = "useful for when you need to translate youtube videos to some language. The country code for this language will be used for translation. It takes youtube url and the country code for translation."

    def _run(self, string: str, run_manager: Optional[CallbackManager] = None) -> str:
        """Use the tool."""
        
        url, country_code = string.split(',')
        country_code= country_code.strip()[0:2]
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()
        try:
           youtube_content = result[0].page_content
           translator = Translator()
           translations = translator.translate(youtube_content, dest=country_code)
           return translations.text
        except:
           return 'No subtitle not found'
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManager] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

def test_tool():
    tool = YoutubeTranslator()
    print(tool.run('https://www.youtube.com/watch?v=a71xD6RyOok&ab_channel=SaregamaMusic, bn')) #Translate to bangla language



def test_agent():
    tools = [
      YoutubeTranslator()
    ]
    llm = ChatOpenAI(temperature=0)
    mrkl = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    print(mrkl.run("Translate the url https://www.youtube.com/watch?v=QsYGlZkevEg to spanish "))
    


def main():
    test_tool()
    #test agent

if __name__==main():
   main()
