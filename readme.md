# Bot de Classficação de Licitações da Pref. de Taboão da Serra (SP).

Este é um script Python que configura um bot do Telegram para **classificar dados de um documento do Google Sheets**. O prejto faz parte do trabalho final da disciplina de **Algoritmos de Automação do Master de Jornalismo de Dados, Automação e Data Storytelling do Insper (SP)**.

---

## Motivação :bulb:

Essa solução de bot foi desenvolvida com a motivação de apoiar o trabalho de jornalismo de dados a partir do conteúdo público disponibilizado pela Prefeitura de Taboão da Serra (SP). 

A análise realizada no trabalho de conclusão do Master em Jornalismo de Dados apontou que a cidade de Taboão da Serra gasta uma quantia significativa de dinheiro em processos que não permitem total transparência, como é o caso da modalidade 'Dispensa de Licitação'. Ao adotar essa postura, a Prefeitura local prejudica a visibilidade das contas públicas. 

Para combater esse problema, foi desenvolvido um bot que, em associação com um scrapper de licitações da Prefeitura de Taboão da Serra, atua como **monitor dos tipos de licitações.**

Dessa forma, o bot pode ajudar a garantir a transparência dos processos licitatórios e contribuir para o trabalho de jornalismo de dados.

---

## Configuração :wrench:

Para usar este script, você precisará fazer o seguinte:

1. Configurar um bot do Telegram e obter sua chave de API.
2. Configurar uma API do Google Sheets e obter as credenciais para acessar o documento desejado.
3. Substitua os valores das variáveis TELEGRAM_API_KEY, TELEGRAM_ADMIN_ID, GOOGLE_SHEETS_CREDENTIALS e planilha_google pela sua própria chave de API, ID do administrador, credenciais e chave do documento do Google Sheets, respectivamente.

---


## Executando o Script :computer:
Para executar o script, basta executá-lo em um ambiente Python. 

O script irá configurar uma aplicação web Flask e ouvir solicitações na endpoint/classificar. 

Quando uma solicitação é recebida, o script irá classificar os dados do documento do Google Sheets e enviar os resultados para o chat do Telegram com o ID especificado pelo parâmetro chat_id na solicitação.

---

## Dependências :clipboard:
Este script depende dos seguintes pacotes Python:

- os
- gspread
- pandas
- oauth2client
- telebot
- requests
- flask

Estes podem ser instalados usando o pip, no caso do Google Colab, ou através do requirements.txt, estratégia abordada aqui.

---

## Dificuldades :no_entry_sign:

Durante o projeto, foram enfrentadas algumas dificuldades, especialmente devido ao uso de uma plataforma desconhecida, como o Render, e a depuração de seus bugs na conta gratuita. 

Isso ocorreu porque há uma **diferença significativa entre a plataforma Google Colab e o Render**, o que tornou o processo de validação de erros mais lento. Embora os testes pudessem ser realizados no ambiente Colab e mitigados, a **validação dos erros levou muito tempo**, o que dificultou bastante a construção do projeto.

Além disso, **o tempo necessário para se familiarizar com a plataforma e o domínio necessário do Python** tornaram mais complexa a aprendizagem e leitura da documentação específica para implementação de códigos e bibliotecas.


---

## Aprendizados :heavy_check_mark:

Essas habilidades listadas são essenciais para o trabalho com desenvolvimento de software e análise de dados.

Entre eles, ter um **maior domínio de strings em Python** permite a manipulação e análise de dados em textos, algo fundamental para diversas aplicações. 

Outro ponto, foi o **melhor entendimento do funcionamento de API's** é importante para realizar a integração de diferentes sistemas e aplicações, permitindo a troca de informações de forma mais eficiente e segura. 

Igualmente, o **conhecimento sobre aplicações de serviço de nuvem** permite o desenvolvimento de soluções escaláveis e com alta disponibilidade, o que é essencial para automações, principalmente no contexto do jornalismo de dados. 

A **melhoria das habilidades de scrapping** é importante para coletar e extrair informações de fontes diversas, o que é fundamental para a análise de dados. 

Por fim, ter um **maior domínio das habilidades com manipulação de dados de um dataframe para o Google Sheets** permite a análise e organização de dados de forma mais eficiente e colaborativa. Todos esses conhecimentos podem ser aplicados em diferentes áreas, como inteligência artificial, análise de dados, desenvolvimento de aplicativos, entre outras.
