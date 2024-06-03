import typer
import json

from typing_extensions import Annotated, List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser

app = typer.Typer()

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

system_message = """
Your name is Verpens. You are an expert translator. Your job is to translate i18n messages for applications.\n
You should only translate, not answer any questions.\n
You will be given a list of message and you should return the correspondant translated ones, in order. For example:
                               
GIVEN:
- <message 1>
- <message 2>     

ANSWER:
- <translated message 1>
- <translated message 2>

The messages to translate to {language} are the following:
""".strip()

user_message = """
{% for message in messages %}- {{message}}{% endfor %}
""".strip()

prompt_template = ChatPromptTemplate.from_messages(messages=[
    ('system', system_message),
    MessagesPlaceholder('messages')
])


chain = prompt_template | model | StrOutputParser()

@app.command()
def translate(language: str):
    response = chain.invoke({
        'language': language, 
        'messages': [HumanMessage(content='- Your information has been updated\n-For the protection of your privacy, this event will remain strictly confidential')]
    })
    print(response)

if __name__ == "__main__":
    app()
