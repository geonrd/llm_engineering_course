"""
This is an excercise from Udemy course 'LLM Engineering: Master AI, Large Language Models & Agents'

https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models
https://github.com/ed-donner/llm_engineering/blob/main/week1/day2%20EXERCISE.ipynb
"""

import ollama
import requests
from bs4 import BeautifulSoup

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.1:latest"

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
        self.summary = ''

    def get_user_prompt(self):
        user_prompt = f"You are looking at a website titled {self.title}"
        user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes code, summarize that too.\n\n"
        user_prompt += self.text
        return user_prompt

    def get_messages(self):
        return [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': self.get_user_prompt()}
        ]

    def summarize(self):
        response = ollama.chat(model=MODEL, messages=self.get_messages())
        self.summary = response['message']['content']
        print("summary saved")
