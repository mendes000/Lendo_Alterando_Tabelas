from pathlib import Path
import streamlit as st
import pandas as pd

# lendo a tabela
pasta_datasets = Path.cwd() / 'datasets'
caminho_vendas = pasta_datasets / 'vendas.csv'

df_vendas = pd.read_csv(caminho_vendas, sep=';', decimal=',', index_col='data')

colunas = list(df_vendas.columns) # lista todas as colunas da tabela

# criando sidebar com opções de seleção
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas', # Label que irá aparecer no campo
                       colunas,     # lista de opções para selecionar
                       colunas)     # valores selecionados por defaut


col1, col2 = st.sidebar.columns(2)  # Cria duas colunas na sidebar
col_filtro = col1.selectbox('Selecione a coluna',
                            [c for c in colunas if c not in ['id_venda']]) # gera a series que será usada como filtro

valor_filtro = col2.selectbox('Selecione o valor',
               list(df_vendas[col_filtro].unique()))  # gera uma lista de valores únicos da coluna selecionada

# criar botões de filtrar e limpar na col1 e col2
status_filtrar = col1.button('Filtrar') # sempre que clicar no botão ele o status passa a ser True
status_limpar = col2.button('Limpar')


# apresentando no navegador

if status_filtrar: # se filtrar = True (botão filtrar clicado)
    st.dataframe(df_vendas.loc[df_vendas[col_filtro]== valor_filtro, # .loc(x,y) x = seleciona linhas
                            # na coluna selecionada no filtro, busca as linhas com valor = valor filtrado
                            colunas_selecionadas],  # y apresenta apenas as colunas selecionadas no outro filtro
                            height= 800) # altura = 800pixels para aumentar a altura da tabela

elif status_limpar: # se não, se limpar = True (botão limpar clicado)
    st.dataframe(df_vendas[colunas_selecionadas],
                 height= 800)
    
else:  # se nem filtrar, nem limpar forem True (nenhum botão clicado)
    st.dataframe(df_vendas[colunas_selecionadas],
                 height= 800)

