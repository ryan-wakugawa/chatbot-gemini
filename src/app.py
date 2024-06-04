import PIL.Image
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
import telebot
from dotenv import load_dotenv, find_dotenv
from IPython.display import Markdown, display
from functions import *
import textwrap
import requests
from google.generativeai.types import HarmCategory,HarmBlockThreshold

class Conta():
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.saldo = 0

load_dotenv()
API_KEY = os.getenv('API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

nomes = []
contas = []
index = -1
        
def getSaldo() -> int:
    return contas[index].saldo

def pagar(nome_da_conta_a_ser_paga: str, valor: int) -> int:
    if contas[index].saldo - valor < 0:
        return f'Saldo insuficiente'
    for conta in contas:
        if conta.nome == nome_da_conta_a_ser_paga:
            conta.saldo += valor
            contas[index].saldo -= valor
    return f'Pagamento de {valor} para {nome_da_conta_a_ser_paga} feito com sucesso'

def receber(valor: int) -> int:
    contas[index].saldo += valor
    return contas[index].saldo
    
def criarConta(nome:str, senha:str):
    contas.append(Conta(nome, senha))
    return f'Conta de {nome} criada com sucesso!'

def login(nome:str, senha:str):
    global index
    for conta in contas:
        if conta.nome == nome and conta.senha == senha:
            index = contas.index(conta)
            return f'Bem vindo {nome}!'
    return f'Conta de {nome} não encontrada!'

def editarConta(nome:str, senha:str):
    global index
    contas[index].nome = nome
    contas[index].senha = senha
    return f'Conta de {nome} editada com sucesso!'

def deletarConta(nome:str, senha:str):
    ##confirme com o usuário se ele realmente deseja deletar a conta
    for conta in contas:
        if conta.nome == nome and conta.senha == senha:
            contas.remove(conta)
            return f'Conta de {nome} deletada com sucesso!'
    return f'Conta de {nome} não encontrada!'

def sair():
    global index
    index = -1
    return 'Você saiu da sua conta'

def listarContas():
    for conta in contas:
        nomes = [].append(conta.nome)
    return nomes

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
genai.configure(api_key=API_KEY)
modelText = genai.GenerativeModel(model_name='gemini-1.5-flash-latest',
                                  tools=[criarConta,listarContas,login,editarConta,deletarConta, getSaldo, pagar, receber],
                                  system_instruction="Você é um assistente de banco que cria contas de usuários, lista as contas, realiza o login das contas, realiza pagamentos e recebe transferências. Para fazer o login em uma conta, sempre exija a senha correta, e se a senha estiver errada, exiba uma mensagem de erro. Nunca exiba as senhas de outros usuários, a não ser que seja a senha da conta logada. Ações de pagamento, edição e recebimento devem ser realizadas apenas se o usuário estiver logado. Se o saldo for menor que 0 após o pagamento, retorne ele para 0 e exiba uma mensagem de erro ao usuário que o saldo é insuficiente. Confirme com o usuário se ele realmente deseja deletar a conta. Não responda qualquer pergunta ou realize qualquer tarefa não relacionada com sua função")
chat = modelText.start_chat(enable_automatic_function_calling=True, history=[])

@bot.message_handler(func=lambda message: True)
def handleText(message):
    try:
        response = chat.send_message(message.text,)
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