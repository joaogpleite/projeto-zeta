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
with open("google_sheets_credentials.json", mode="w") as fobj:
    fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("google_sheets_credentials.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")  # Replace with your Google Sheets key
sheet = planilha.worksheet("lic1")  # Replace with the name of your worksheet

# Set up Flask app
app = Flask(__name__)

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    if "message" not in update:
        return "ok"  # Not a message, ignore it
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    if message == "/start":
        bot.send_message(chat_id, "Olá, para classificar as licitações digite /classificar")
    elif message == "/classificar":
        chamada_publica = sheet.count("Chamada Pública")
        convite = sheet.count("Convite")
        dispensa = sheet.count("Dispensa de Licitação")
        encerrada = sheet.count("encerrada")
        aberto = sheet.count("em aberto")
        andamento = sheet.count("andamento")
        response = f"Aquí estão as licitações classificadas por Modalidade e Situação:\n" \
                   f"Chamada Pública: {chamada_publica}\n" \
                   f"Convite: {convite}\n" \
                   f"Dispensa de Licitação: {dispensa}\n" \
                   f"Encerrada: {encerrada}\n" \
                   f"Em aberto: {aberto}\n" \
                   f"Andamento: {andamento}"
        bot.send_message(chat_id, response)
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)

