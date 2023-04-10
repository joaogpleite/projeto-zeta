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

def coleta_dados_view():
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df[['Modalidade', 'Situação']]
    print(df.columns)

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
        df = coleta_dados_view()
        modalidades = df['Modalidade'].value_counts()
        finalidades = df['Finalidade/Objeto/Serviço'].value_counts()
        situacoes = df['Situação'].value_counts()
        dispensa = modalidades.get('Dispensa de Licitação', 0)
        chamada = modalidades.get('Chamada Pública', 0)
        convite = modalidades.get('Convite', 0)
         
        andamento = situacoes.get('andamento', 0)
        aberto = situacoes.get('em aberto', 0)
        encerrada = situacoes.get('encerrada', 0)
        
        response = f"Aqui estão as licitações classificadas por Modalidade e Situação:\n" \
                   f"Chamada Pública: {chamada}\n" \
                   f"Convite: {convite}\n" \
                   f"Dispensa de Licitação: {dispensa}\n" \
                   f"Encerrada: {encerrada}\n" \
                   f"Em aberto: {aberto}\n" \
                   f"Andamento: {andamento}"
        bot.send_message(chat_id, response)
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
