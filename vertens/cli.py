import typer
import json

from pathlib import Path
from typing import List, Optional
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
Message could contains interpolation values, which are bound in double brackets, like {{number}}. These values should be kept as-is but you can however translate the rest.
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
    output: Path, 
    language: Annotated[str, typer.Option(help="Target language")],
    batch_size: Annotated[int, typer.Option(help="Number of messages sent to LLM per batch")] = 100,
    sample_size: Annotated[Optional[int], typer.Option(help="Run only on first sample_size. It might be helpful for test.")] = None,
    placeholder: Annotated[Optional[str], typer.Option(help="If a message has this placeholder value, it is meant to be translated")] = "__STRING_NOT_TRANSLATED__"
):
    with open(input, 'r') as file:
        source = json.loads(file.read(), object_pairs_hook=OrderedDict)
    
    target = OrderedDict[str, str]()
    if output.exists():
        with open(output, 'r') as file:
            target = json.loads(file.read(), object_pairs_hook=OrderedDict)

    items = [
        item for item in source.items() 
        if ((key := item[0]) not in target) or (target[key] == placeholder)
    ]
    
    if sample_size and sample_size < len(items):
        items = items[:sample_size]

    for batch in chunked(items, batch_size):
        keys = [item[0] for item in batch]
        ms = [item[1] for item in batch]
        ts = run(language, ms)
        for (k, v) in zip(keys, ts):
            target[k] = v
    
    with open(output, 'w') as file:
        json.dump(target, file, ensure_ascii=False, indent=2)

        
def run(language: str, messages: List[str]) -> List[str]:
    response = chain.invoke({
        'language': language, 
        'messages': [HumanMessage(content='\n'.join(f"- {msg}" for msg in messages))]
    })
    translated = [ line[1:].strip() for line in response.split("\n") ]
    return translated


if __name__ == "__main__":
    app()
