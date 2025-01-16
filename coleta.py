import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processamento import *
# from mensagem_whatsapp import *
import asyncio  # Importando asyncio para rodar o código assíncrono
from mensagem_telegram import filtrar_e_enviar_excel
from datetime import datetime  # Importando datetime para manipular datas
from db import processar_e_salvar


def acessar_site():
    # Caminho correto para o ChromeDriver
    chromedriver_path = r'C:\Users\uriel\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe'

    # Configurando o serviço do ChromeDriver
    service = Service(chromedriver_path)
    options = Options()

    # Inicializando o WebDriver com o serviço configurado
    driver = webdriver.Chrome(service=service, options=options)

    # Acessando a URL
    url = "https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp"
    driver.get(url)

    # Aguardando a página carregar completamente
    driver.implicitly_wait(10)

    print("Página carregada com sucesso!")

    # Usando WebDriverWait para garantir que o elemento esteja visível antes de interagir
    try:
        # **Alteração aqui**: Esperar o elemento aparecer
        selecionar_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="cmb_estado"]'))
        )
        selecionar_button.click()

        # Selecionando a opção 'Todos'
        todos_option = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//select[@id="cmb_estado"]/option[text()="Todos"]'))
        )
        todos_option.click()

        # Clicar para fazer o download
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="btn_next1"]'))
        )
        download_button.click()

    except Exception as e:
        print(f"Erro ao interagir com o site: {e}")

    # Pausando para garantir o download
    time.sleep(20)

    # **Alteração aqui**: Fechar o navegador ao final
    driver.quit()

    # Caminho onde o arquivo foi baixado (confirme o nome do arquivo baixado)
    caminho_arquivo = r'C:\Users\uriel\Downloads\Lista_imoveis_geral.csv'

    # Mover o arquivo baixado para o novo caminho com a data
    os.rename(r'C:\Users\uriel\Downloads\Lista_imoveis_geral.csv', caminho_arquivo)
    return caminho_arquivo


if __name__ == "__main__":
    arquivo_baixado = acessar_site()
    print(f"Arquivo baixado: {arquivo_baixado}")

    # # Passando o arquivo baixado para o próximo passo
    # from processamento import tratar_e_carregar
    # tratar_e_carregar(arquivo_baixado)

    # # Chamar a função de envio (a função do segundo script) após o processamento
    # # Caminho do arquivo processado
    # arquivo_processado = r'C:\Users\uriel\Downloads\Lista_imoveis_tratada_novo.xlsx'
    # estado = 'MG'  # O estado que você deseja filtrar
    # valor_maximo = 140000  # O valor máximo para o filtro

    # # Salvar os dados no banco de dados.
    # processar_e_salvar(arquivo_processado)

    # # Chama a função assíncrona para enviar o arquivo
    # asyncio.run(filtrar_e_enviar_excel(
    #     arquivo_processado, estado, valor_maximo))
