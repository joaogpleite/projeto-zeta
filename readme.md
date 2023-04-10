Este é um script Python que configura um bot do Telegram para classificar dados de um documento do Google Sheets.

---

## Configuração
Para usar este script, você precisará fazer o seguinte:

1. Configurar um bot do Telegram e obter sua chave de API.
2. Configurar uma API do Google Sheets e obter as credenciais para acessar o documento desejado.
3. Substitua os valores das variáveis TELEGRAM_API_KEY, TELEGRAM_ADMIN_ID, GOOGLE_SHEETS_CREDENTIALS e planilha_google pela sua própria chave de API, ID do administrador, credenciais e chave do documento do Google Sheets, respectivamente.

---


## Executando o Script
Para executar o script, basta executá-lo em um ambiente Python. O script irá configurar uma aplicação web Flask e ouvir solicitações na endpoint /classificar. Quando uma solicitação é recebida, o script irá classificar os dados do documento do Google Sheets e enviar os resultados para o chat do Telegram com o ID especificado pelo parâmetro chat_id na solicitação.

---

## Dependências
Este script depende dos seguintes pacotes Python:

- os
- gspread
- pandas
- oauth2client
- telebot
- requests
- flask

Estes podem ser instalados usando o pip, no caso do Google Colab, ou através do requirements.txt, estratégia abordada aqui.
