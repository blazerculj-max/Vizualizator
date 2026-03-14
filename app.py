import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prodajni Vizualizator: Finančna Varnost", layout="wide")

st.title("🛡️ Diagnostika finančne varnosti in vrzeli")
st.markdown("---")

# VNOSI V STRANSKI VRSTICI
with st.sidebar:
    st.header("👤 Finančni podatki")
    mesecni_prihodek = st.number_input("Mesečni neto prihodek (€)", value=2000, step=100)
    letni_prihodek = mesecni_prihodek * 12
    
    kredit = st.number_input("Preostanek vseh kreditov (€)", value=80000, step=5000)
    prihranki = st.number_input("Trenutni prihranki (€)", value=5000)

# IZRAČUNI
# 1. Bolniška (80% dohodka)
bolniska_izplacilo = mesecni_prihodek * 0.8
izpad_mesecno = mesecni_prihodek - bolniska_izplacilo

# 2. Formule za zavarovalne vsote (po tvojih navodilih)
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# --- PRIKAZ 1: BOLNIŠKA (Takojšnja realnost) ---
st.subheader("📉 Takojšen vpliv na življenjski slog (Bolniška)")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Polna plača", f"{mesecni_prihodek:,.0f} €")
with c2:
    st.metric("Nadomestilo (80%)", f"{bolniska_izplacilo:,.0f} €", delta=f"-{izpad_mesecno:,.0f} €", delta_color="inverse")
with c3:
    st.warning(f"Vsak mesec bolniške vam v proračunu zmanjka **{izpad_mesecno:,.0f} €**.")

st.markdown("---")

# --- PRIKAZ 2: DOLGOROČNA VARNOST (Grafi) ---
st.subheader("📊 Potrebna zaščita za varno prihodnost družine")

def narisi_graf(naslov, vrednost, barva, max_val):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vrednost,
        title = {'text': naslov, 'font': {'size': 20}},
        gauge = {'axis': {'range': [0, max_val]},
                 'bar': {'color': barva},
                 'steps': [
                     {'range': [0, vrednost], 'color': "rgba(255, 0, 0, 0.1)"}
                 ]}
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

col1, col2 = st.columns(2)
limit = potreba_invalidnost + 20000

with col1:
    st.plotly_chart(narisi_graf("Kritje za primer SMRTI", vrzel_smrt, "#31333F", limit), use_container_width=True)
    st.info(f"**Logika:** 3x letni prihodek + krediti. To omogoči družini 3 leta prilagoditve in poplačilo dolgov.")

with col2:
    st.plotly_chart(narisi_graf("Kritje za INVALIDNOST", vrzel_invalidnost, "#FF4B4B", limit), use_container_width=True)
    st.error(f"**Logika:** 6x letni prihodek + krediti. Invalidnost zahteva več sredstev zaradi stroškov oskrbe in trajnega izpada.")

st.markdown("---")

# --- PRIKAZ 3: PRIMERJAVA S CENAMI ---
st.subheader("☕ Investicija v mirno spanje")
# Informativna dnevna premija
dnevna_investicija = (vrzel_invalidnost / 100000) * 1.10 # Okvirno 1.1€ na 100k kritja

cc1, cc2 = st.columns([2, 1])
with cc1:
    st.markdown(f"""
    ### Zakaj so te številke pomembne?
    V primeru 100% invalidnosti bi vaša družina potrebovala **{vrzel_invalidnost:,.0f} €**, da bi ohranila trenutni standard. 
    Brez ustrezne police ta dolg prevzamejo vaši najbližji.
    """)
with cc2:
    st.metric("Dnevni strošek zaščite", f"{dnevna_investicija:.2f} €")
    st.write("To je manj kot stane kava ali prigrizek v avtomatu.")
