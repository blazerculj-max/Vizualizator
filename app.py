import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Coach Kalkulator: Varnostna Vrzel", layout="wide")

st.title("🛡️ Diagnostika prodajne vrzeli: Smrt & Invalidnost")
st.markdown("---")

# VNOSI V STRANSKI VRSTICI
with st.sidebar:
    st.header("👤 Podatki o stranki")
    letni_prihodek = st.number_input("Letni neto prihodek zakonca (€)", value=25000, step=1000)
    kredit = st.number_input("Preostanek vseh kreditov (€)", value=100000, step=5000)
    prihranki = st.number_input("Trenutni prihranki (€)", value=10000)
    
    st.markdown("---")
    st.subheader("🎯 Coach kotiček: DISC")
    tip = st.selectbox("Tip stranke:", ["D", "I", "S", "C"])
    nasveti = {
        "D": "Bodi kratek. Pokaži primanjkljaj in takojšnjo rešitev.",
        "I": "Poudari, kako bo družina ohranila standard (status).",
        "S": "Govori o miru, varnosti in zaščiti gnezda.",
        "C": "Poudari logiko formule (3x in 6x prihodek)."
    }
    st.info(nasveti[tip])

# FORMULA: Izračun potreb po tvojih navodilih
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# VIZUALIZACIJA
col1, col2 = st.columns(2)

def narisi_graf(naslov, vrednost, barva):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vrednost,
        title = {'text': naslov},
        gauge = {'axis': {'range': [0, potreba_invalidnost + 50000]},
                 'bar': {'color': barva}}
    ))
    return fig

with col1:
    st.subheader("💀 Scenarij: Smrt")
    st.plotly_chart(narisi_graf("Potrebno kritje (€)", vrzel_smrt, "#31333F"), use_container_width=True)
    st.write(f"Formula: ({letni_prihodek:,.0f}€ * 3) + {kredit:,.0f}€ dolga")

with col2:
    st.subheader("♿ Scenarij: 100% Invalidnost")
    st.plotly_chart(narisi_graf("Potrebno kritje (€)", vrzel_invalidnost, "#FF4B4B"), use_container_width=True)
    st.write(f"Formula: ({letni_prihodek:,.0f}€ * 6) + {kredit:,.0f}€ dolga")

st.markdown("---")

# PRIMERJAVA S CENAMI (Visual Anchoring)
st.subheader("☕ Kaj to pomeni za vaš žep?")
c1, c2, c3 = st.columns(3)

# Informativni izračun premije (0.7€ na 100k za smrt, 1.2€ na 100k za invalidnost - okvirno)
ocenjena_mesecna = (vrzel_smrt / 100000 * 7) + (vrzel_invalidnost / 100000 * 12)
dnevna = ocenjena_mesecna / 30

with c1:
    st.metric("Skupna vrzel (Najhujši scenarij)", f"{vrzel_invalidnost:,.0f} €")
with c2:
    st.metric("Dnevna investicija v varnost", f"{dnevna:.2f} €")
with c3:
    if dnevna < 2.0:
        st.success("Cena je nižja od ene kave dnevno!")
    else:
        st.warning("Investicija v varnost je še vedno manjša od stroška kosila.")

st.markdown(f"### 💡 Prodajni nasvet za tip {tip}:")
st.write(f"Stranki pokaži razliko med grafoma. Invalidnost je **2x dražja** za družino kot smrt, ker zakonec ostane doma in potrebuje oskrbo, prihodka pa ni.")
