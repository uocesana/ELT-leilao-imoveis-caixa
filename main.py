import asyncio
from coleta import acessar_site
from processamento import tratar_e_carregar
from db import processar_e_salvar
from mensagem_telegram import filtrar_e_enviar_excel
import os
import time

# Desativa os logs de aviso e info do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main():
    try:
        tempo_inicio_total = time.time()

        # Passo 1: Baixar o arquivo
        print("Iniciando download do arquivo...")
        tempo_inicio_etapa = time.time()
        arquivo_baixado = acessar_site()
        tempo_etapa = (time.time() - tempo_inicio_etapa) / 60
        print(f"Arquivo baixado: {arquivo_baixado}")
        print(f"Tempo para download: {tempo_etapa:.2f} segundos\n")

        # Passo 2: Processar o arquivo
        print("Iniciando processamento...")
        tempo_inicio_etapa = time.time()
        arquivo_processado = tratar_e_carregar(arquivo_baixado)
        tempo_etapa = (time.time() - tempo_inicio_etapa) / 60
        print(f"Tempo para processamento: {tempo_etapa:.2f} segundos\n")

        if arquivo_processado is None:
            print("Erro no processamento do arquivo.")
            return

        # Passo 3: Salvar no banco de dados
        print("Salvando dados no banco...")
        tempo_inicio_etapa = time.time()
        processar_e_salvar(arquivo_processado)
        tempo_etapa = (time.time() - tempo_inicio_etapa) / 60
        print(f"Tempo para salvar no banco: {tempo_etapa:.2f} segundos\n")

        # Passo 4: Enviar mensagens via Telegram
        estado = 'MG'
        valor_maximo = 140000

        print("Enviando dados via Telegram...")
        tempo_inicio_etapa = time.time()
        asyncio.run(filtrar_e_enviar_excel(
            arquivo_processado, estado, valor_maximo))
        tempo_etapa = (time.time() - tempo_inicio_etapa) / 60
        print(f"Tempo para envio no Telegram: {tempo_etapa:.2f} segundos\n")

        # Tempo total
        tempo_total = (time.time() - tempo_inicio_total) / 60
        print(f"\nTempo total decorrido: {tempo_total:.2f} segundos")

    except Exception as e:
        print(f"Ocorreu um erro no processo: {e}")


if __name__ == "__main__":
    main()
