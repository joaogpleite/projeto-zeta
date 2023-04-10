import os
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

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

# Define function to scrape data from Google Sheets and classify it
def classificar(update, context):
    # Get data from Google Sheets
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Count occurrences of keywords in "Modalidade" and "Situação" columns
    modalidade_counts = df["Modalidade"].str.count("Dispensa de Licitação|Chamada Pública|Convite").sum()
    situacao_counts = df["Situação"].str.count("encerrada|andamento|em aberto").sum()
    
    # Send message with counts to user
    message = f"Dispensa de Licitação: {modalidade_counts}\nChamada Pública: {modalidade_counts}\nConvite: {modalidade_counts}\n-----------------------------------\nAndamento: {situacao_counts}\nEm aberto: {situacao_counts}\nEncerrada: {situacao_counts}"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

# Set up Telegram handler for "/classificar" command
bot.add_command_handler("classificar", classificar)

# Start the bot
bot.polling()

