import streamlit as st
import requests
import json
import BuscarCep
import pandas as pd

    ##--- TÍTULO DA APLICAÇÃO 
st.image('principal.png')
st.title('Buscando o seu CEP')


    ##--- Lista de opções 
opcoes = ["Buscar CEP", "Descobrir CEP"]

    ##--- BARRA LATERAL
st.sidebar.title('Busca CEP')
st.sidebar.image('logo.png', width=400)
escolha = st.sidebar.selectbox('Selecione uma opção', opcoes)


    ##--- BUSCAR CEP
if escolha == 'Buscar CEP':
    st.header('Buscar Endereço pelo CEP')
    cep = st.text_input('Digite o CEP (somente números):')

    if st.button('Buscar'):
        cep_limpo = cep.replace('-', '').strip()
        if len(cep_limpo) != 8 or not cep_limpo.isdigit():
            st.error('Por favor, insira um CEP válido com 8 dígitos numéricos.')
        else:
            try:
                endereco = BuscarCep.buscar_cep(cep_limpo)
                if endereco:
                    st.success('Endereço encontrado:')
                    st.write(f'📌 **CEP:** {endereco[0]}')
                    st.write(f'🏠 **Endereço:** {endereco[1]}')
                    st.write(f'🏘️ **Bairro:** {endereco[2]}')
                    st.write(f'🌆 **Cidade:** {endereco[3]}')
                    st.write(f'🗺️ **Estado:** {endereco[4]}')


    ##---Mapa
                    st.subheader('Localização no Mapa')
                    df = pd.DataFrame({'latitude': [endereco[5]], 'longitude': [endereco[6]]})
                    st.map(df, zoom=15)
                else:
                    st.error('CEP não encontrado.')
            except Exception as e:
                st.error(f'Ocorreu um erro ao buscar o CEP: {e}')


    
    ##--- DESCOBRIR CEP
elif escolha == 'Descobrir CEP':
    st.header('Descobrir o CEP pelo Endereço')
    st.markdown('Informe os dados abaixo para localizar o CEP correspondente.')

    col1, col2 = st.columns(2)
    with col1:
        uf = st.text_input('Estado (UF)', max_chars=2).upper()
    with col2:
        cidade = st.text_input('Cidade').title()

    logradouro = st.text_input('Nome da rua, avenida ou logradouro')

    if uf and cidade and logradouro:
        if len(uf) != 2 or not uf.isalpha():
            st.warning('O campo "Estado (UF)" deve conter exatamente 2 letras.')
        else:
            try:
                endereco_completo = f"{logradouro}, {cidade}, {uf}"
                resultado = BuscarCep.descobrir_cep(endereco_completo)
                if resultado:
                    st.success('CEP(s) encontrado(s):')
                    for item in resultado:
                        st.write(f"📍 **CEP:** {item['cep']} — {item['logradouro']}, {item['bairro']} — {item['localidade']}/{item['uf']}")
                else:
                    st.info('Nenhum CEP foi encontrado com os dados informados.')
            except Exception as e:
                st.error(f'Ocorreu um erro ao tentar descobrir o CEP: {e}')
    else:
        st.info('Por favor, preencha todos os campos acima para realizar a busca.')

    st.image('Descobrir.png', use_container_width=True)