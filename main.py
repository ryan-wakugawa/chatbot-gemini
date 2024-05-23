prompt = 'Me diga a receita de um mousse de chocolate'

import PIL.Image
img = PIL.Image.open('baked_goods_2.jpg')

import google.generativeai as genai
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