import os

import gspread
import requests
import telebot
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
bot = telebot.TeleBot(TELEGRAM_API_KEY)
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as fobj:
  fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) 
planilha = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")
sheet = planilha.worksheet("lic1")
app = Flask(__name__)

@bot.message_handler(commands=['classificar'])
def classify(message):
    # open the Google Sheets document
    sheet = client.open_by_url(doc_url).sheet1

    # get the values from the cells and create a pandas DataFrame
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    # Classify the data
    modalidades = df['Modalidade'].value_counts()
    finalidades = df['Finalidade/Objeto/Serviço'].value_counts()
    situacoes = df['Situação'].value_counts()

    dispensa = modalidades.get('Dispensa de Licitacao', 0)
    chamada = modalidades.get('Chamada Publica', 0)
    convite = modalidades.get('Convite', 0)

    andamento = situacoes.get('andamento', 0)
    aberto = situacoes.get('em aberto', 0)
    encerrada = situacoes.get('encerrada', 0)

    # send the response to the user
    response = f"Dispensa de Licitação: {dispensa}\n"
    response += f"Chamada Pública: {chamada}\n"
    response += f"Convite: {convite}\n"
    response += f"-----------------------------------\n"
    response += f"Andamento: {andamento}\n"
    response += f"Em aberto: {aberto}\n"
    response += f"Encerrada: {encerrada}"
    bot.send_message(message.chat.id, response)

# define the bot command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Olá, para classificar a sua planilha digite classificar")

def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado


menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">Promocoes</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (João Gabriel)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"


@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
    return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Joao", "Leite", "a partir do Flask"])
  return "Planilha escrita!"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id": chat_id, "text": message}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"
  
