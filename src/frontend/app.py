import streamlit as st
import requests


st.set_page_config(page_title="Diário Oficial - Sebrae", layout="wide")


API_BASE_URL = "http://app:8000"


st.subheader("Diário Oficial - Sebrae")
data_selecionada = st.date_input("Escolha a data da publicação")


if st.button("Buscar Notícias"):
    with st.spinner("Buscando notícias no banco de dados..."):
        response = requests.get(f"{API_BASE_URL}/noticias-por-data/{data_selecionada}")
        st.session_state.lista_noticias = response.json()


if "lista_noticias" in st.session_state and st.session_state.lista_noticias:
    options = {n["noticia"]: n["id"] for n in st.session_state.lista_noticias}
    escolha = st.selectbox("Selecione a notícia:", list(options.keys()))
    id_escolhido = options[escolha]

    if st.button("Explicar Notícia"):
        with st.spinner("Consultando a IA (processando explicação)..."):
            resp = requests.get(f"{API_BASE_URL}/explicar/{id_escolhido}")
            st.session_state.dados_explicacao = resp.json()
            st.session_state.id_atual = id_escolhido


if "dados_explicacao" in st.session_state:
    st.markdown("---")
    st.write(st.session_state.dados_explicacao["explicacao_inteligente"])

    if st.button("🖼️ Gerar Infográfico (Cartão)"):
        with st.spinner("Gerando cartão..."):
            res = requests.post(f"{API_BASE_URL}/gerar-cartao/{st.session_state.id_atual}")
            caminho = res.json().get("caminho_cartao")
            if caminho:
                st.image(caminho)
                st.success("Cartão gerado com sucesso!")
            else:
                st.error("Não foi possível gerar o cartão (verifique wkhtmltoimage).")

