"""
This is an excercise from Udemy course 'LLM Engineering: Master AI, Large Language Models & Agents' showing
how easy it is to make a simple interface for a model

For streaming output from openai, use stream_answer_openai()
For all-at-once response from ollama, use get_answer_ollama()

https://github.com/ed-donner/llm_engineering/blob/main/week1/week1%20EXERCISE.ipynb
https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import ollama
from IPython.display import Markdown, display, update_display


MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"
OLLAMA_API = "http://localhost:11434/api/chat"

system_prompt = "You are a highly intelligent and resourceful assistant that gives accurate answers to people asking technical questions."

question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')


def stream_answer_openai(user_prompt):
    openai = OpenAI()
    stream = openai.chat.completions.create(
        model=MODEL_GPT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```", "").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)


def get_answer_ollama(user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = ollama.chat(model=MODEL_LLAMA, messages=messages)
    content = response['message']['content']
    display(Markdown(content))

#stream_answer_openai(question)
get_answer_ollama(question)
