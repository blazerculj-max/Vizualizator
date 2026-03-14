import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Analiza finančne varnosti", layout="wide")

st.title("🛡️ Vizualizator finančne vrzeli")
st.subheader("Ugotovite, kolikšen znesek zavarovanja dejansko potrebuje vaša družina.")

# Sidebar za vnose (Inputi)
with st.sidebar:
    st.header("Vaši podatki")
    mesecni_stroski = st.slider("Mesečni stroški družine (€)", 500, 5000, 1500)
    leta_podpore = st.slider("Leta kritja (npr. do osamosvojitve otrok)", 1, 25, 10)
    kredit = st.number_input("Preostanek kredita (€)", value=50000)
    
    st.header("Obstoječi viri")
    prihranki = st.number_input("Trenutni prihranki (€)", value=5000)
    drzavno_nadomestilo = st.slider("Ocenjeno državno nadomestilo (mesečno €)", 0, 1000, 400)

# Izračuni
skupne_potrebe = (mesecni_stroski * 12 * leta_podpore) + kredit
skupni_viri = (drzavno_nadomestilo * 12 * leta_podpore) + prihranki
vrzel = skupne_potrebe - skupni_viri
