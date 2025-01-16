# processamento.py
from pathlib import Path
import pandas as pd
import warnings

warnings.simplefilter("ignore")
pd.set_option('display.max_columns', None)


def carregar_dados(arquivo_csv):
    """Carrega o arquivo CSV e normaliza as colunas."""
    df = pd.read_csv(arquivo_csv, encoding='latin1', sep=';', skiprows=2)
    df.columns = (
        df.columns
        .str.normalize('NFKD')
        .str.encode('ASCII', errors='ignore')
        .str.decode('ASCII')
        .str.strip()
    )
    df = df.drop(index=[0, 1, 3])  # Remove as linhas desnecessárias
    return df


def extrair_descricao(desc, pos, sep=',', split_pos=1, default=None):
    """Extrai partes específicas da descrição."""
    try:
        return desc.split(sep)[pos].split(' ')[split_pos]
    except IndexError:
        return default


def limpar_e_converter(valor):
    """Limpa e converte valores numéricos."""
    try:
        return float(valor.replace('.', '').replace(',', '.'))
    except (ValueError, AttributeError):
        return None


def tratar_e_carregar(arquivo_csv):
    """Processa e salva o arquivo tratado."""
    df = carregar_dados(arquivo_csv)

    # Seleção e renomeação de colunas
    nomes_campos_tradados = df[
        ['N do imovel', 'UF', 'Cidade', 'Bairro', 'Preco',
         'Valor de avaliacao', 'Desconto', 'Descricao',
         'Modalidade de venda', 'Link de acesso']
    ].rename(columns={
        'N do imovel': 'numero_imovel',
        'UF': 'uf',
        'Cidade': 'cidade',
        'Bairro': 'bairro',
        'Preco': 'preco',
        'Valor de avaliacao': 'valor_avaliacao',
        'Desconto': 'desconto',
        'Descricao': 'descricao',
        'Modalidade de venda': 'modalidade_venda',
        'Link de acesso': 'link_acesso'
    })
    nomes_campos_tradados['uf'] = nomes_campos_tradados['uf'].str.strip()
    # Adicionar colunas processadas
    nomes_campos_tradados['imovel'] = nomes_campos_tradados['descricao'].str.split(
        ',').str[0]
    nomes_campos_tradados['metro_quadrado_m3'] = nomes_campos_tradados['descricao'].apply(
        lambda x: extrair_descricao(x, 2))
    nomes_campos_tradados['metro_quadrado_area_total_m3'] = nomes_campos_tradados['descricao'].apply(
        lambda x: extrair_descricao(x, 3))

    # Conversão de colunas
    colunas_para_converter = ['preco', 'valor_avaliacao',
                              'metro_quadrado_m3', 'metro_quadrado_area_total_m3']
    nomes_campos_tradados[colunas_para_converter] = nomes_campos_tradados[colunas_para_converter].applymap(
        limpar_e_converter)

    # Seleção final e exportação
    colunas_finais = [
        'numero_imovel', 'uf', 'cidade', 'bairro', 'preco',
        'valor_avaliacao', 'desconto', 'modalidade_venda',
        'imovel', 'metro_quadrado_m3', 'metro_quadrado_area_total_m3', 'link_acesso'
    ]
    consolidado = nomes_campos_tradados[colunas_finais]
    consolidado['data_processamento'] = pd.Timestamp.now()

    # Salvar em ExcelSSSS
    arquivo_saida = Path(
        r'C:\Users\uriel\Downloads\Lista_imoveis_tratada_novo.xlsx')
    consolidado.to_excel(arquivo_saida, index=False,
                         sheet_name='lista_imoveis')

    print("Processamento concluído e arquivo salvo com sucesso!")
    return arquivo_saida
