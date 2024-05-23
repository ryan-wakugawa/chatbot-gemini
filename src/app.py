import PIL.Image
import google.generativeai as genai
import os
import telebot
from dotenv import load_dotenv, find_dotenv
from IPython.display import Markdown, display
import textwrap
import requests

listaCadastro = []

def cadastrar(input:str):
    listaCadastro.append(input)
    
def mostrarCadastros() -> list:
    return listaCadastro

load_dotenv()
API_KEY = os.getenv('API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='MARKDOWN')
genai.configure(api_key=API_KEY)
modelText = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', tools=[cadastrar, mostrarCadastros])
modelImage = genai.GenerativeModel(model_name='gemini-pro-vision')
chat = modelText.start_chat(enable_automatic_function_calling=True, history=[])

@bot.message_handler(func=lambda message: True)
def handleText(message):
    try:
        response = chat.send_message(message.text)
        bot.reply_to(message, response.text)
        for content in chat.history:
            part = content.parts[0]
            print(content.role, "->", type(part).to_dict(part))
            print('-'*60)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        
@bot.message_handler(content_types=['photo'])
def handleImage(photo):
    try:
        bot.reply_to(photo, 'teste')
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
bot.polling()