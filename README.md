# Vertens

Automatic translation of i18n messages for your products.

Large language models are particularly good at languages. Let's use them to quickly make our products fully localized for international audiences.

## Features
- Multiple languages
- Models: OpenAI GPT. Others coming soon.
- Batch support to fit into LLM context size
- Keys order is preserved as the input. This is important for version control.

## Installation

WIP

## How to use

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