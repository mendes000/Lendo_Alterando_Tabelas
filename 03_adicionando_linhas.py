from pathlib import Path
import streamlit as st
import pandas as pd
import ast
from datetime import datetime

# lendo as planilhas
pasta_datasets = Path.cwd() / 'datasets'

df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', sep=';', decimal=',', index_col=0)
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', sep=';', decimal=',')
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', sep=';', decimal=',')

# criando selectbox de cidade/estado
df_filiais['cidade/estado'] = df_filiais['cidade']+ '/' + df_filiais['estado']

lista_filiais = df_filiais['cidade/estado'].to_list() # transforma series em lista
filial_selecionada = st.sidebar.selectbox('Selecione uma cidade', lista_filiais)

# criando selectbox de vendedores baseado na cidade/estado selecionada anteiormente
lista_vendedores = df_filiais.loc[df_filiais['cidade/estado']== filial_selecionada,
                                     'vendedores']
vendedores_str = lista_vendedores.iloc[0] # É uma lista que parece uma string
vendedores = ast.literal_eval(vendedores_str) # ast.literal_eval # converte uma string que parece lista em uma lista real
vendedor_selecionado = st.sidebar.selectbox('Selecione um vendedor', vendedores)

# criando selectbox de produtos
lista_produtos = df_produtos['nome'].to_list()
produtos_selecionado = st.sidebar.selectbox('Escolha um produto', lista_produtos)

# adicionando dados a tabela
nome_cliente = st.sidebar.text_input('Nome do Cliente')

# adicionando gênero do cliente
genero_cliente = st.sidebar.selectbox('Gênero do Cliente', ['masculino', 'feminino'])

# adicionando forma de pagamento
forma_pgto = st.sidebar.selectbox('Forma de pagamento', ['pix', 'crédito', 'boleto'])

# criando botão para adicionar nova venda
if st.sidebar.button('Adicionar nova venda'):
    lista_adicionar = [df_vendas['id_venda'].max() + 1,  # necessário colocar a mesma qtde de colunas
                       filial_selecionada,
                       vendedor_selecionado,
                       produtos_selecionado,
                       nome_cliente,
                       genero_cliente,
                       forma_pgto]
    df_vendas.loc[datetime.now()] = lista_adicionar # na leitura do df_vendas foi colocado a coluna 'data' como índice
                                                    # com isso, qdo ele busca a coluna com data e hora atual e não encontra
                                                    # ele cria uma nova, adicionando os demais itens listados na lista_adicionar
    df_vendas.to_csv(pasta_datasets / 'vendas.csv', sep=';', decimal=',')
    st.success('Venda Adicionada')


st.dataframe(df_vendas, height= 800)