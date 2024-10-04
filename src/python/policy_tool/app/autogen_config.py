import autogen
import os

gpt4_config = {
    "seed": 41852,  # change the seed for different trials
    "temperature": 0,
    "config_list": [{"model": "gpt-4", "api_key": os.environ['OPENAI_API_KEY']}]
}