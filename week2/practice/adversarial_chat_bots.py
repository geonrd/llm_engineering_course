import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display
import google.generativeai
import ollama

# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

openai = OpenAI()
google.generativeai.configure()
MODEL_OLLAMA = "llama3.2"
OLLAMA_API = "http://localhost:11434/api/chat"

# ollama_model = "llama3.2"
openai_model = "gpt-4o-mini"
gemini_model = "gemini-2.0-flash-exp"

#ollama_system = "You are a chatbot named Albert that loves talking about sports. Whenever you can, you try to relate the conversation to sports. there are 3 people total in the conversation. you just met them and are standing in line at the grocery store."
openai_system = "You are a chatbot named Bart with the personality of a diva lumberjack. You don't like taking guff from anyone. Loves cooking but not necessarily people. there are 2 people total in the conversation. you just met them and are standing in line at the grocery store."
gemini_system = "You are a chatbot named Carl that loves to fish... for compliments. there are 2 people total in the conversation. you just met them and are standing in line at the grocery store."

#ollama_messages = ["Yo, what's up!"]
openai_messages = ["Hey"]
gemini_messages = ["Uh, hi?"]

def call_openai():
    messages = [{'role': 'system', 'content': openai_system}]
    for  openai_msg, gemini_msg in zip( openai_messages, gemini_messages):
        messages.append({"role": "assistant", "content": openai_msg})
        #messages.append({"role": "user", "content": ollama_msg})
        messages.append({"role": "user", "content": gemini_msg})
    response = openai.chat.completions.create(
        model=openai_model,
        messages = messages
    )
    return response.choices[0].message.content

# def call_ollama():
#     messages = [{'role': 'system', 'content': ollama_system}]
#     for ollama_msg, openai_msg, gemini_msg in zip(ollama_messages, openai_messages, gemini_messages):
#         messages.append({"role": "assistant", "content": ollama_msg})
#         messages.append({'role': 'user', 'content': openai_msg})
#         messages.append({'role': 'user', 'content': gemini_msg})
#     response = ollama.chat(model=MODEL_OLLAMA, messages=messages)
#     return response['message']['content']

def call_gemini():
    #messages = [{'role': 'system', 'content': gemini_system}]
    messages = []
    for  openai_msg, gemini_msg in zip( openai_messages, gemini_messages):
        messages.append({'role': 'assistant', 'parts': gemini_msg})
        messages.append({'role': 'user', 'parts': openai_msg})
        #messages.append({'role': 'user', 'parts': ollama_msg})
    gemini = google.generativeai.GenerativeModel(
        model_name='gemini-2.0-flash-exp',
        system_instruction=gemini_system
    )
    response = gemini.generate_content(messages)
    return response.text


def main():
    for i in range(3):
        # ollama_next = call_ollama()
        # print(f"Llama:\n{ollama_next}\n")
        # ollama_messages.append(ollama_next)
        openai_next = call_openai()
        print(f"OpenAI:\n{openai_next}\n")
        openai_messages.append(openai_next)
        gemini_next = call_gemini()
        print(f"Gemini:\n{gemini_next}\n")
        gemini_messages.append(gemini_next)

# this is a very dumb conversation, because I've set it up for each to take a turn per round, which is not
# exactly how conversations go. a more natural flow would analyze the output to look for clues as to which
# bot the bot is responding to. I should also add some kind of element of randomness in who speaks next.
