# inserir_imoveis.py
import pandas as pd
import mysql.connector
from mysql.connector import Error
from credenciais import host, user, password, database


def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conexao.is_connected():
            print("Conectado ao MySQL com sucesso!")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def salvar_no_mysql(df):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        try:
            valores = [tuple(row.astype(str)) for _, row in df.iterrows()]

            query = '''INSERT INTO lista_imoveis (
                numero_imovel, uf, cidade, bairro, preco,
                valor_avaliacao, desconto, modalidade_venda,
                imovel, metro_quadrado_m3,
                metro_quadrado_area_total_m3, link_acesso, data_processamento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            cursor.executemany(query, valores)
            conexao.commit()
            print(f"{len(df)} registros salvos com sucesso no MySQL!")
        except Error as e:
            print(f"Erro ao salvar no MySQL: {e}")
            conexao.rollback()
        finally:
            cursor.close()
            conexao.close()


def processar_e_salvar(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    df = df.fillna('').astype(str)
    salvar_no_mysql(df)
