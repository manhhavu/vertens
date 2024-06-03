import typer
import json

from pathlib import Path
from typing import List
from typing_extensions import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser
from more_itertools import chunked
from collections import OrderedDict

app = typer.Typer()

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

system_message = """
Your name is Verpens. You are an expert translator. Your job is to translate i18n messages for applications.\n
You should only translate, not answer any questions.\n
Message could contains placeholder values, which are bound in double brackets, like {{number}}. These values should be kept as-is but you can however translate the rest.
You will be given a list of message and you should return the correspondant translated ones, in order. 
                               
GIVEN:
- <message 1>
- <message 2>     

ANSWER:
- <translated message 1>
- <translated message 2>

The messages to translate to {language} (language code) are the following:
""".strip()

prompt_template = ChatPromptTemplate.from_messages(messages=[
    ('system', system_message),
    MessagesPlaceholder('messages')
])

chain = prompt_template | model | StrOutputParser()

@app.command()
def translate(
    input: Path, 
    output_dir: Path, 
    language: Annotated[List[str], typer.Option(help="Target language(s)")],
    batch_size: Annotated[int, typer.Option(help="Number of messages sent to LLM per batch")] = 100
):
    with open(input, 'r') as file:
        source = json.loads(file.read(), object_pairs_hook=OrderedDict)
    
    for lang in language:
        translated: OrderedDict[str, str] = OrderedDict()
        for batch in chunked(source.items(), batch_size):
            keys = [item[0] for item in batch]
            ms = [item[1] for item in batch]
            ts = run(lang, ms)
            for (k, v) in zip(keys, ts):
                translated[k] = v
    
        with open(output_dir / f'lang-{lang}.json', 'w') as file:
            json.dump(translated, file, ensure_ascii=False, indent=2)

        
def run(language: str, messages: List[str]) -> List[str]:
    response = chain.invoke({
        'language': language, 
        'messages': [HumanMessage(content='\n'.join(f"- {msg}" for msg in messages))]
    })
    translated = [ line[1:].strip() for line in response.split("\n") ]
    return translated


if __name__ == "__main__":
    app()
