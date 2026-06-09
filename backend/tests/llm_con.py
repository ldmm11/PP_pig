# Please install OpenAI SDK first: `pip3 install openai`
import os
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 加载 backend/.env 中的环境变量
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(env_path)

def test_llm():
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model=getenv('DEEPSEEK_MODEL'),
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hello, I am a helpful assistant"},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
)
    res = response.choices[0].message.content
    print(res)


if __name__ == '__main__':
    test_llm()
