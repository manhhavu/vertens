# Vertens

Automatic translation of i18n messages for your products with AI.

Large language models are particularly good at languages. Let's use them to quickly make our products fully localized for international audiences.

## Features
- Support multiple target languages as long as the LLM support
- Idempotency: 
    - Only translated missing keys in target language, do nothing otherwise.
    - Keys order is preserved as the input. This is important for version control.
- Models: OpenAI GPT. Others coming soon.
- Batch support to fit into LLM context size

## Backlog
- Support other file formats: properties, gettext

## Installation

WIP

## Basic usage

Before running **vertens**, you need have an [OpenAI key](https://platform.openai.com/api-keys) configured as an environment variable OPENAI_API_KEY.

Given an input file in this format:

```json
{
    "key1": "Message 1",
    "key2": "Message 2",
}
```

The following command translate **input.json** to **fr, de** languages. The result for each language is written into its own file in the output directory.

```bash
vertens --language fr --language de <path/to/input.json> <path/to/output_directory>
```

You can also view other parameters with help

```bash
vertens --help
```

## Recipes

### (React) i18next messages

[i18next](https://www.i18next.com/) is a popular i18n solution, especially for ReactJS.

Vertens currently support only JSON format which has top level keys, like

{
    "key1": "Message 1",
    "key2": "Message 2",
}

but not deep nested keys, like:

{
    "key1" : {
        "key11": ""
    }
}

You can write a script to transform between these formats so that you can use
with Vertens.

We can translate the top level keys format as:

```bash
vertens --language fr ./lang-en.json ./lang-fr.json
```

You can also specify a placeholder value to specify which messages to be translated 
if its key is already present in the target language file.

```bash
vertens --language fr --placeholder __STRING_NOT_TRANSLATED__ ./lang-en.json ./lang-fr.json
```

This is typically useful if you are using a tool like [i18next-scanner](https://github.com/i18next/i18next-scanner) which 
is very cool. It scans messages to translate or remove (if no longer used)

### Translate multiple languages

A loop in Bash would serve this purpose

```bash
#!/usr/bin/env bash

for lang in fr de
do
    vertens --language $lang ./lang-en.json ./lang-$lang.json
done
```

### Smoke runs

If you have a huge translation file, and you want to test the vertens without
translating all of them, you can use the **--sample-size** parameter to pick only
a small portion of the file to translate.