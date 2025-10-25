import streamlit as st
import requests
import pandas as pd
from PIL import Image

# Função para pegar a bandeira via emoji
def bandeira(paisCodigo):
    if len(paisCodigo) != 2:
        return ""
    return chr(ord(paisCodigo[0].upper()) + 127397) + chr(ord(paisCodigo[1].upper()) + 127397)

# Configuração da página
st.set_page_config(
    page_title="Painel de Nomes", 
    page_icon="pngs/PA_Sobre1-661441c5055fb.png", 
    layout="centered"
)

# -----------------------------
# LOGO NO TOPO
# -----------------------------
try:
    logo = Image.open("logo.png")  # Substitua pelo nome do seu arquivo de logo
    st.image(logo, width=200)
except:
    st.write("Logo não encontrada.")

# -----------------------------
# Título e descrição
# -----------------------------
st.title("FATEC PORTAS ABERTAS:NOMES 🎲")
st.write("Descubra curiosidades sobre o seu nome com dados reais!")

# Entrada do usuário
nome = st.text_input("Digite um nome:")

# -----------------------------
# Pesquisa de dados
# -----------------------------
if nome:
    try:
        # Chamadas das APIs públicas
        genero = requests.get(f"https://api.genderize.io?name={nome}").json()
        idade = requests.get(f"https://api.agify.io?name={nome}").json()
        pais = requests.get(f"https://api.nationalize.io?name={nome}").json()

        st.subheader(f"📊 Resultados para '{nome.capitalize()}'")

        # Exibe o gênero
        if genero.get("gender"):
            st.write(f"👤 Gênero provável: **{genero['gender']}** ({genero['probability']*100:.1f}%)")
        else:
            st.write("👤 Gênero não identificado.")

        # Exibe a idade média
        if idade.get("age"):
            st.write(f"🎂 Idade média: **{idade['age']} anos**")
        else:
            st.write("🎂 Idade média não disponível.")

        # Exibe os países de origem com bandeiras
        if pais.get("country"):
            st.write("🌍 Países mais prováveis de origem:")

            # DataFrame para gráfico
            df = pd.DataFrame(pais["country"])
            df["probability"] = df["probability"] * 100
            df = df.rename(columns={"country_id": "País", "probability": "Probabilidade (%)"})
            st.bar_chart(df.set_index("País"))

            # Lista detalhada com bandeiras
            for c in pais["country"]:
                cod = c["country_id"]
                prob = c["probability"] * 100
                st.write(f"{bandeira(cod)} {cod} — {prob:.1f}%")
        else:
            st.write("🌍 Nenhuma origem detectada para esse nome.")

    except Exception as e:
        st.error("⚠️ Ocorreu um erro ao buscar os dados. Verifique sua conexão.")
        st.text(e)

# -----------------------------
# Rodapé
# -----------------------------
st.markdown("---")
st.caption("Projeto educacional desenvolvido em Python • FATEC ADS")
