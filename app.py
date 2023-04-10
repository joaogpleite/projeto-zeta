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
sheet = planilha.worksheet("lic1")  # Replace with the name of your worksheet


# Set up Flask app
app = Flask(__name__)

    
  @app.route("/telegram-bot", methods=["POST"])
  def telegram_bot():
    update = request.json
  for update in dados:
    update_id = update["update_id"]
    if "message" not in update:
      print(f"ERROR: not a menssagem: {update}")
      continue
    # Extrai dados para mostrar mensagem recebida
    first_name = update["message"]["from"]["first_name"]
    sender_id = update["message"]["from"]["id"]
    if "text" not in update["message"]:
      continue  # Essa mensagem não é um texto!
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    datahora = str(datetime.datetime.fromtimestamp(update["message"]["date"]))
    if "username" in update["message"]["from"]:
      username = update["message"]["from"]["username"]
    else:
      username = "[não definido]"
    print(f"[{datahora}] Nova mensagem de {first_name} @{username} ({chat_id}): {message}")
    mensagens.append([datahora, "recebida", username, first_name, chat_id, message])
    # Define qual será a resposta e envia
    if message == "/start":
      texto_resposta = "Olá! Seja bem-vinda(o). *Digite* /noticias para ver as últimas."
    else:
      texto_resposta = "Não entendi!"
    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  
    # Return a response to indicate that the request was processed successfully
    return "ok"

