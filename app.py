import os

import pandas as pd
import gspread
import requests
import telebot
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials


# Set up the Telegram bot
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
bot = telebot.TeleBot(TELEGRAM_API_KEY)
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]


# Set up Google Sheets API
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("insperautomacao-joao", mode="w") as fobj:
    fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("insperautomacao-joao")
api = gspread.authorize(conta)
planilha = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")  # Replace with your Google Sheets key
sheet = planilha.worksheet("Planilha_1")  # Replace with the name of your worksheet


# Set up Flask app
app = Flask(__name__)


# Handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    response = "Olá, para classificar a sua planilha digite /classificar"
    bot.send_message(message.chat.id, response)


# Handle the /classificar command
@app.route("/classificar", methods=["POST"])
def classificar():
    # Get data from the Google Sheets document
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

    # Send the response to the user
    response = f"Dispensa de Licitação: {dispensa}\n"
    response += f"Chamada Pública: {chamada}\n"
    response += f"Convite: {convite}\n"
    response += f"-----------------------------------\n"
    response += f"Andamento: {andamento}\n"
    response += f"Em aberto: {aberto}\n"
    response += f"Encerrada: {encerrada}"
    chat_id = request.json["message"]["chat"]["id"]
    bot.send_message(chat_id, response)

    # Return a response to indicate that the request was processed successfully
    return "ok"

