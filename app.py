import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import telebot
import requests
from flask import Flask, request

# Set up the Telegram bot
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
bot = telebot.TeleBot(TELEGRAM_API_KEY)
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

# Set up Google Sheets API
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as fobj:
    fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha_google = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")  # Replace with your Google Sheets key
sheet = planilha_google.worksheet("lic1")  # Replace with the name of your worksheet

app = Flask(__name__)

@app.route("/telegram-bot", methods=['POST'])

@app.route("/")
def index():
    return "olá" #print(resultado_scraper)

# Define a route to handle the /start command
@app.route('/start', methods=['POST'])
def start_command():
    # Get the chat ID of the user who sent the message
    chat_id = request.json['message']['chat']['id']

    # Send a message to the user
    response_text = "Olá! Para classificar as licitações digite /classificar"
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage', json={'chat_id': chat_id, 'text': response_text})

    return 'OK'

# Define a route to handle the /classificar command
@app.route('/classificar', methods=['POST'])
def classificar_command():
    # Get the chat ID of the user who sent the message
    chat_id = request.json['message']['chat']['id']

    # Get the data from the Google Sheets document
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Classify the data
    modalidade_counts = df[df["Modalidade"].str.contains("Dispensa de Licitação|Chamada Pública|Convite")]["Modalidade"].value_counts()
    situacao_counts = df[df["Situação"].str.contains("encerrada|andamento|em aberto")]["Situação"].value_counts()

    # Format the message
    response_text = f"Modalidade:\n{modalidade_counts}\n\nSituação:\n{situacao_counts}"

    # Send the message to the user
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage', json={'chat_id': chat_id, 'text': response_text})

    return 'OK'

