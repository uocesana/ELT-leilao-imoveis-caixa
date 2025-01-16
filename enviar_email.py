import pandas as pd
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from credenciais import SMTP_SERVER, SMTP_PORT, EMAIL_USUARIO, EMAIL_SENHA

# Configuração do servidor Gmail
SMTP_SERVER = SMTP_SERVER
SMTP_PORT = SMTP_PORT
EMAIL_USUARIO = EMAIL_USUARIO
EMAIL_SENHA = EMAIL_SENHA


def filtrar_e_enviar_excel(arquivo_entrada, estado, valor_maximo):
    arquivo_entrada = Path(arquivo_entrada)

    if not arquivo_entrada.exists():
        print(f"Erro: O arquivo {arquivo_entrada} não foi encontrado!")
        return

    # Ler o arquivo Excel
    df = pd.read_excel(arquivo_entrada)

    # Filtrar os dados
    df_filtrado = df[(df['uf'] == estado) & (df['preco'] <= valor_maximo)]

    if len(df_filtrado) == 0:
        print("Nenhum registro encontrado após aplicar os filtros.")
        return

    # Ordenar e pegar os 10 primeiros
    df_filtrado = df_filtrado.sort_values(by='preco').head(10)

    # Salvar o arquivo filtrado
    arquivo_filtrado = 'imoveis_filtrados.xlsx'
    df_filtrado.to_excel(arquivo_filtrado, index=False)

    # Enviar e-mail com anexo
    destinatario = EMAIL_USUARIO
    assunto = "Relatório de Imóveis Filtrados"
    corpo = "Segue em anexo a lista de imóveis filtrados."

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USUARIO
        msg["To"] = destinatario
        msg["Subject"] = assunto

        # Adicionar o corpo do e-mail
        msg.attach(MIMEText(corpo, "plain"))

        # Anexar o arquivo Excel
        with open(arquivo_filtrado, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            f"attachment; filename={arquivo_filtrado}")
            msg.attach(part)

        # Conectar ao servidor e enviar o e-mail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USUARIO, EMAIL_SENHA)
        server.send_message(msg)
        server.quit()

        print(f"E-mail enviado com sucesso para {destinatario}!")

    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")


# Definindo o caminho do arquivo e executando a função
if __name__ == "__main__":
    arquivo_processado = r'C:\Users\uriel\Downloads\Lista_imoveis_tratada_novo.xlsx'
    filtrar_e_enviar_excel(arquivo_processado, 'MG', 140000)
