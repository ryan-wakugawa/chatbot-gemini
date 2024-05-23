import PIL.Image
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

API_KEY = os.getenv('API_KEY')

prompt = 'Me diga a receita de um mousse de chocolate'

img = PIL.Image.open('baked_goods_2.jpg')

from IPython.display import Markdown, clear_output, display

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name='gemini-pro')
response = model.generate_content([prompt], stream=True)

buffer = []
for chunk in response:
    for part in chunk.parts:
        buffer.append(part.text)
    clear_output()
    display(Markdown(''.join(buffer)))