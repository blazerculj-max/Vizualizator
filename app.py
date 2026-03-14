import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prodajni Vizualizator: Finančni Impact", layout="wide")

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

# 2. Scenarij HUDA BOLEZEN (3-letni vpliv)
# Leto 1 & 2: 80% bolniška (izpad 20% vsako leto)
izpad_leto_1_2 = (mesecni_prihodek * 0.2) * 24 
# Leto 3: Polovični delovni čas (izpad 50% prihodka)
izpad_leto_3 = (mesecni_prihodek * 0.5) * 12
skupni_izpad_huda_bolezen = izpad_leto_1_2 + izpad_leto_3

# 3. Formule za zavarovalne vsote (po tvojih navodilih)
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# --- PRIKAZ 1: HUDA BOLEZEN (Realističen scenarij 3 let) ---
st.subheader("⚠️ Scenarij: Huda bolezen (Rehabilitacija)")
col_a, col_b = st.columns([1, 2])

with col_a:
    st.write("Potek:")
    st.write("- **Leto 1 & 2:** Bolniška (80 %)")
    st.write("- **Leto 3:** Polovični delovni čas (50 %)")
    st.metric("Skupni izpad prihodka", f"-{skupni_izpad_huda_bolezen:,.0f} €", delta_color="inverse")

with col_b:
    # Vizualizacija izpada skozi čas
    meseci = list(range(1, 37))
    prihodek_po_mesecih = [bolniska_izplacilo]*24 + [mesecni_prihodek * 0.5]*12
    
    fig_hb = go.Figure()
    fig_hb.add_trace(go.Scatter(x=meseci, y=prihodek_po_mesecih, fill='tozeroy', name='Dejanski prihodek', line_color='red'))
    fig_hb.add_hline(y=mesecni_prihodek, line_dash="dash", annotation_text="Vaša polna plača")
    fig_hb.update_layout(title="Padanje prihodkov v 3 letih", xaxis_title="Mesec", yaxis_title="Prihodek (€)", height=300)
    st.plotly_chart(fig_hb, use_container_width=True)

st.markdown("---")

# --- PRIKAZ 2: DOLGOROČNA VARNOST (Grafi) ---
st.subheader("📊 Potrebna zaščita za varno prihodnost družine")

def narisi_graf(naslov, vrednost, barva, max_val):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vrednost,
        title = {'text': naslov, 'font': {'size': 20}},
        gauge = {'axis': {'range': [0, max_val]},
                 'bar': {'color': barva}}
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

col1, col2 = st.columns(2)
limit = potreba_invalidnost + 20000

with col1:
    st.plotly_chart(narisi_graf("Kritje za primer SMRTI", vrzel_smrt, "#31333F", limit), use_container_width=True)
    st.caption(f"Formula: (3x Letni prihodek) + Krediti - Prihranki")

with col2:
    st.plotly_chart(narisi_graf("Kritje za INVALIDNOST", vrzel_invalidnost, "#FF4B4B", limit), use_container_width=True)
    st.caption(f"Formula: (6x Letni prihodek) + Krediti - Prihranki")

st.markdown("---")

# --- ZAKLJUČEK ---
st.info(f"💡 **Ključna ugotovitev:** Samo huda bolezen brez trajne invalidnosti bi vašo družino stala **{skupni_izpad_huda_bolezen:,.0f} €**. Ali imate ta znesek trenutno na računu?")
