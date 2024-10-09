from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
import yaml
import os
import json
import pandas as pd
from openai import OpenAI
from pathlib import Path

client = OpenAI()

promptfile = Path('prompts/eligibility-ExOffer-few-shot.txt')

def get_prompt(filename: Path) -> str:
    with open(filename, 'r') as f:
        system_prompt = f.read()
    return system_prompt

def extract_structured_rules(input: str, system_prompt: str, client: OpenAI = client):
    """Given the text of an Action, return a JSON document of the eligibility rules according to the schema in the system prompt"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": input,
            }
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content