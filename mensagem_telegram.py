import pandas as pd
from telegram import Bot
from pathlib import Path
import asyncio
from datetime import datetime
from credenciais import TOKEN, CHAT_ID

# Defina o token do bot e o chat_id (obtenha isso criando um bot no @BotFather)
TOKEN = TOKEN
CHAT_ID = CHAT_ID

# Inicializar o bot corretamente com a nova abordagem
bot = Bot(token=TOKEN)


async def filtrar_e_enviar_excel(arquivo_entrada, estado, valor_maximo):
    arquivo_entrada = Path(arquivo_entrada)

    if not arquivo_entrada.exists():
        # print(f"Erro: O arquivo {arquivo_entrada} não foi encontrado!")
        return

    # Ler o arquivo Excel
    df = pd.read_excel(arquivo_entrada)

    # Exibir as primeiras linhas para verificar se os dados estão corretos
    # print(f"Primeiras linhas do arquivo: \n{df.head()}")

    # Filtrar os dados com base no estado e valor máximo
    df_filtrado = df[(df['uf'] == estado) & (df['preco'] <= valor_maximo)]

    # Exibir o número de registros após o filtro
    # print(f"Número de registros após filtro: {len(df_filtrado)}")

    # Se não houver registros filtrados, notificar e interromper
    if len(df_filtrado) == 0:
        # print("Nenhum registro encontrado após aplicar os filtros.")
        return

    # Ordenar e pegar os 10 primeiros
    df_filtrado = df_filtrado.sort_values(by='preco').head(10)

    # Exibir as primeiras linhas dos dados filtrados
    # print(f"Primeiras linhas dos dados filtrados: \n{df_filtrado.head()}")

    campos_desejados = ['uf', 'cidade', 'bairro', 'preco', 'valor_avaliacao',
                        'desconto', 'metro_quadrado_m3', 'metro_quadrado_area_total_m3', 'link_acesso']
    df_filtrado = df_filtrado[campos_desejados]

    # Salvar o arquivo filtrado
    arquivo_filtrado = 'imoveis_filtrados.xlsx'
    df_filtrado.to_excel(arquivo_filtrado, index=False)

    # Enviar a mensagem
    mensagem = "Aqui estão os 10 imóveis selecionados no estado de MG com valores até R$ 140.000,00."
    await bot.send_message(chat_id=CHAT_ID, text=mensagem)

    # Enviar o arquivo Excel
    with open(arquivo_filtrado, 'rb') as file:
        await bot.send_document(chat_id=CHAT_ID, document=file)

    print("Arquivo enviado com sucesso!")


# Definindo o caminho do arquivo e executando a função
if __name__ == "__main__":
    arquivo_processado = r'C:\Users\uriel\Downloads\Lista_imoveis_tratada_novo.xlsx'
    asyncio.run(filtrar_e_enviar_excel(arquivo_processado, 'MG', 140000))
