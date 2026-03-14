import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prodajni Vizualizator: Varnostna Vrzel", layout="wide")

st.title("🛡️ Diagnostika finančne varnosti in vrzeli")
st.markdown("---")

# VNOSI V STRANSKI VRSTICI
with st.sidebar:
    st.header("👤 Finančni podatki")
    mesecni_prihodek = st.number_input("Mesečni neto prihodek (€)", value=2000, step=100)
    letni_prihodek = mesecni_prihodek * 12
    
    kredit = st.number_input("Preostanek vseh kreditov (€)", value=80000, step=5000)
    prihranki = st.number_input("Trenutna likvidna sredstva (€)", value=5000)

# IZRAČUNI
# 1. Bolniška: Bolezen (80%) vs Nezgoda (70%)
bolniska_bolezen = mesecni_prihodek * 0.8
bolniska_nezgoda = mesecni_prihodek * 0.7

izpad_bolezen = mesecni_prihodek - bolniska_bolezen
izpad_nezgoda = mesecni_prihodek - bolniska_nezgoda

# Predvideno dnevno nadomestilo, da pokrijemo izpad pri nezgodi
# Izračun: Izpad nezgoda / 30 dni
potrebno_dnevno_nadomestilo = izpad_nezgoda / 30

# 2. Scenarij HUDA BOLEZEN (3-letni vpliv)
izpad_leto_1_2 = (mesecni_prihodek * 0.2) * 24 
izpad_leto_3 = (mesecni_prihodek * 0.5) * 12
skupni_izpad_huda_bolezen = izpad_leto_1_2 + izpad_leto_3

# 3. Formule za zavarovalne vsote
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# --- PRIKAZ 1: PRIMERJAVA BOLNIŠKE (Bolezen vs Nezgoda) ---
st.subheader("📉 Takojšen izpad prihodka (Mesečno)")
c1, c2, c3 = st.columns(3)

with c1:
    st.info(f"**Polna plača:** {mesecni_prihodek:,.0f} €")

with c2:
    st.error(f"**Bolezen (80%):** {bolniska_bolezen:,.0f} €")
    st.caption(f"Primanjkljaj: -{izpad_bolezen:,.0f} €/mesec")

with c3:
    st.error(f"**Nezgoda (70%):** {bolniska_nezgoda:,.0f} €")
    st.caption(f"Primanjkljaj: -{izpad_nezgoda:,.0f} €/mesec")

# Dnevno nadomestilo
st.markdown(f"""
> 💡 **Prodajni namig:** Da bi stranka ob nezgodi ohranila standard (2.000 €), potrebuje zavarovano dnevno nadomestilo v višini vsaj **{potrebno_dnevno_nadomestilo:.2f} €/dan**.
""")

st.markdown("---")

# --- PRIKAZ 2: HUDA BOLEZEN (Realističen scenarij 3 let) ---
st.subheader("⚠️ Scenarij: Huda bolezen (3-letna rehabilitacija)")
col_a, col_b = st.columns([1, 2])

with col_a:
    st.write("- **Leti 1 & 2:** 80% bolniška")
    st.write("- **Leto 3:** 50% skrajšan delovnik")
    st.metric("Skupni izpad prihodka", f"-{skupni_izpad_huda_bolezen:,.0f} €")

with col_b:
    meseci = list(range(1, 37))
    prihodek_po_mesecih = [bolniska_bolezen]*24 + [mesecni_prihodek * 0.5]*12
    fig_hb = go.Figure()
    fig_hb.add_trace(go.Scatter(x=meseci, y=prihodek_po_mesecih, fill='tozeroy', name='Dejanski prihodek', line_color='red'))
    fig_hb.add_hline(y=mesecni_prihodek, line_dash="dash", annotation_text="Polna plača")
    fig_hb.update_layout(title="Padanje prihodkov", height=250, margin=dict(t=30, b=0))
    st.plotly_chart(fig_hb, use_container_width=True)

st.markdown("---")

# --- PRIKAZ 3: DOLGOROČNA VARNOST (Grafi) ---
st.subheader("📊 Kapitalna zaščita (Smrt in Invalidnost)")

def narisi_graf(naslov, vrednost, barva, max_val):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = vrednost,
        title = {'text': naslov, 'font': {'size': 18}},
        gauge = {'axis': {'range': [0, max_val]}, 'bar': {'color': barva}}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

col1, col2 = st.columns(2)
limit = potreba_invalidnost + 20000

with col1:
    st.plotly_chart(narisi_graf("Kritje za primer SMRTI", vrzel_smrt, "#31333F", limit), use_container_width=True)
    st.caption(f"Formula: (3x Letni prihodek) + Dolgovi")

with col2:
    st.plotly_chart(narisi_graf("Kritje za INVALIDNOST", vrzel_invalidnost, "#FF4B4B", limit), use_container_width=True)
    st.caption(f"Formula: (6x Letni prihodek) + Dolgovi")
