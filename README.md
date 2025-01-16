# ETL - Imóveis de Leilão: Extração, Tratamento, Carga e Visualização dos Dados com Python, Streamlit e Looker Studio

**Data:** 16/01/2025  
**Autor:** Uriel Cesana  
**Local:** Três Lagoas, MS, 79620-386  

---

## Visão Geral

Este projeto tem o objetivo de desenvolver um fluxo de dados automatizado para coletar, processar, armazenar, notificar e visualizar, de forma inteligente, informações sobre imóveis em leilão da Caixa Econômica Federal. O projeto visa facilitar a análise e o acompanhamento de oportunidades de investimento em uma variedade de imóveis espalhados por todo o Brasil.

---

## Etapas do Fluxo de Dados

### 1. Fonte de Dados (Extração)
- Os dados são extraídos da página oficial da Caixa Econômica Federal, contendo informações sobre imóveis em leilão.
- A extração é realizada via **Script Python** que realiza o download dos dados em formato **CSV** e armazena em diretório local.

### 2. Transformação e Processamento
- Após a coleta, os dados são processados utilizando **Python** para:
  - Remover campos irrelevantes;
  - Adicionar campo de **Data de Processamento**;
  - Converter o arquivo para formato **XLSX**.
- Realizar filtros, como imóveis com valor de até **R$ 140.000,00** e localizados em **Minas Gerais**.
- Um arquivo com os filtros de interesse é gerado para uso posterior em notificações de oportunidade via **Telegram**, **WhatsApp** e **E-mail**.

### 3. Carga e Armazenamento (MySQL)
- Os dados processados são carregados em um banco de dados **MySQL**, permitindo o armazenamento de dados históricos e uma consulta estruturada.
- O banco de dados está hospedado em uma instância **EC2** da **AWS**.

### 4. Notificação Automática
- Um conjunto de notificações de oportunidades é enviado em diferentes canais utilizando **Python**.
- Canais de notificação incluem:
  - **Telegram**
  - **WhatsApp**
  - **E-mail**
- As notificações incluem informações resumidas e links para acessar os detalhes completos dos imóveis.

### 5. Visualização de Dados

#### Visualização de Dados usando **Streamlit**
- Um Relatório Completo é disponibilizado ao usuário que, uma vez conectado ao banco de dados MySQL, consome, em tempo real, todos os dados relacionados aos imóveis de oportunidade espalhados pelo Brasil.
- O Relatório permite a exploração visual dos dados em:
  - **Cards**;
  - **Visuais de barras verticais**;
  - **Tabelas**;
  - **Mapa de Bolhas**.

#### Visualização de Dados usando **Looker Studio**
- Um Relatório Completo desenvolvido utilizando **Looker Studio** (Google) é disponibilizado ao usuário.
- A plataforma torna a interação mais flexível para usuários com nenhum conhecimento de código, permitindo a criação de visuais de acordo com suas necessidades. O relatório consome os dados diretamente do banco de dados MySQL.

---

## Tecnologias Utilizadas

### Linguagens e Ferramentas:
- **Python**
- **Selenium**
- **Streamlit**
- **MySQL**
- **DBeaver**
- **Scheduler Windows**
- **Git/GitHub**
- **Telegram / WhatsApp / Gmail**

### Infraestrutura:
- **AWS EC2 Windows**

---

## Frequência de Atualização | Fluxo

A rotina de atualização dos dados, desde o processo de extração, tratamento, carga no banco de dados, notificação e disponibilização dos relatórios está agendada para ocorrer todos os dias às **07h00 AM**.

O fluxo ocorre executando a partir do **Scheduler Windows** um arquivo **.py** principal, sendo eles:
- `main.py`
- `coleta.py`
- `processamento.py`
- `db.py`
- `mensagem_telegram.py`
- `mensagem_whatsapp.py`
- `enviar_email.py`
- `dash.py`

O fluxo inteiro de atualização, desde o processo de extração, processamento, tratamento, carga e envio de notificações, totalizou **0,88 segundos**.

---

## Repositório do GitHub

[Link para o repositório GitHub](https://github.com/uocesana/ELT-leilao-imoveis-caixa)

---

## Link do Relatório Looker Studio

[Relatório Imóveis de Leilão - Looker Studio](https://lookerstudio.google.com/)

---

Esse é o README em Markdown para o seu projeto. Basta copiar e colar no arquivo `README.md` do seu repositório!
