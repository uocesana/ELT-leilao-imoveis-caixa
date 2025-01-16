import pandas as pd
import pywhatkit as kit
from pathlib import Path
import time
import pyautogui
from credenciais import contato


def filtrar_e_enviar_arquivo(arquivo_entrada, estado, valor_maximo, numeros):
    if not arquivo_entrada.exists():
        print(f"Erro: O arquivo {arquivo_entrada} não foi encontrado!")
        return

    df = pd.read_excel(arquivo_entrada)
    df_filtrado = df[(df['uf'] == estado) & (df['preco'] <= valor_maximo)]
    df_filtrado = df_filtrado.sort_values(by='preco').head(10)

    campos_desejados = ['cidade', 'bairro', 'preco', 'valor_avaliacao', 'desconto',
                        'metro_quadrado_m3', 'metro_quadrado_area_total_m3', 'link_acesso']
    df_filtrado = df_filtrado[campos_desejados]

    # Construção da mensagem
    mensagens = []
    mensagem_base = f"Aqui estão os imóveis em {
        estado} com valores até R$ {valor_maximo:,}:\n\n"
    mensagem_atual = mensagem_base

    for _, row in df_filtrado.iterrows():
        linha = (f"Cidade: {row['cidade']}, Bairro: {row['bairro']}, "
                 f"Preço: R$ {row['preco']}, Desconto: {row['desconto']}%,\n"
                 f"Link: {row['link_acesso']}\n\n")

        # Garantir que a mensagem não ultrapasse o limite do WhatsApp
        if len(mensagem_atual + linha) > 3000:  # Limite de caracteres para uma única mensagem
            mensagens.append(mensagem_atual)
            mensagem_atual = mensagem_base + linha
        else:
            mensagem_atual += linha

    # Adicionar a última mensagem ao lote
    if mensagem_atual:
        mensagens.append(mensagem_atual)

    # Enviar cada mensagem separadamente para cada número
    for numero in numeros:
        try:
            for msg in mensagens:
                kit.sendwhatmsg_instantly(f"+{numero}", msg, wait_time=10)
                time.sleep(5)
                pyautogui.press('enter')
                print(f"Mensagem enviada para {numero}!")
                # Pequeno delay entre cada mensagem para evitar bloqueios
                time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {numero}: {e}")
        time.sleep(5)


if __name__ == "__main__":
    numeros = contato
    arquivo_processado = Path(
        r'C:\Users\uriel\Downloads\Lista_imoveis_tratada_novo.xlsx')
    filtrar_e_enviar_arquivo(arquivo_processado, 'MG', 140000, numeros)
