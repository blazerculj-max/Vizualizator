import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prodajni Vizualizator: Preživetvena Vrzel", layout="wide")

st.title("🛡️ Diagnostika finančne varnosti: Preživetveni model")
st.markdown("---")

# VNOSI V STRANSKI VRSTICI
with st.sidebar:
    st.header("👤 Finančni podatki")
    mesecni_prihodek = st.number_input("Mesečni neto prihodek (€)", value=2000, step=100)
    mesecni_stroski = st.number_input("Nujni mesečni stroški (Kredit, hrana, položnice) (€)", value=1700, step=100)
    
    st.markdown("---")
    kredit = st.number_input("Preostanek vseh kreditov (€)", value=80000, step=5000)
    prihranki = st.number_input("Trenutni prihranki (€)", value=5000)

# IZRAČUNI
# 1. Bolniška: Bolezen (80%) vs Nezgoda (70%)
bolniska_bolezen = mesecni_prihodek * 0.8
bolniska_nezgoda = mesecni_prihodek * 0.7

# Mesečni manjko (Razlika med polno plačo in bolniško)
manjko_bolezen = mesecni_prihodek - bolniska_bolezen
manjko_nezgoda = mesecni_prihodek - bolniska_nezgoda

# Potrebno dnevno nadomestilo samo za NEZGODO
nadomestilo_nezgoda = manjko_nezgoda / 30

# 2. Vzdržnost prihrankov (Mesečna vrzel glede na stroške)
vrzel_stroski_bolezen = max(0, mesecni_stroski - bolniska_bolezen)
vrzel_stroski_nezgoda = max(0, mesecni_stroski - bolniska_nezgoda)

def izracunaj_mesece(prihranki, vrzel):
    if vrzel <= 0: return "Varnost zagotovljena"
    return round(prihranki / vrzel, 1)

meseci_varnosti_bolezen = izracunaj_mesece(prihranki, vrzel_stroski_bolezen)
meseci_varnosti_nezgoda = izracunaj_mesece(prihranki, vrzel_stroski_nezgoda)

# 3. Scenarij HUDA BOLEZEN (3-letni vpliv)
izpad_leto_1_2 = (mesecni_prihodek * 0.2) * 24 
izpad_leto_3 = (mesecni_prihodek * 0.5) * 12
skupni_izpad_huda_bolezen = izpad_leto_1_2 + izpad_leto_3

# 4. Formule za zavarovalne vsote
letni_prihodek = mesecni_prihodek * 12
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# --- PRIKAZ 1: MESEČNI MANJKO IN VZDRŽNOST PRIHRANKOV ---
st.subheader("📉 Analiza izpada dohodka in vzdržnost prihrankov")
c1, c2, c3 = st.columns(3)

with c1:
    st.info("📌 **Status quo**")
    st.write(f"Polna plača: **{mesecni_prihodek:,.0f} €**")
    st.write(f"Nujni stroški: **{mesecni_stroski:,.0f} €**")
    st.write(f"Prihranki: **{prihranki:,.0f} €**")

with c2:
    st.warning("🤒 **Bolezen (80%)**")
    st.write(f"Mesečni manjko: **-{manjko_bolezen:,.0f} €**")
    if isinstance(meseci_varnosti_bolezen, str):
        st.success("Prihranki niso ogroženi.")
    else:
        st.metric("Prihranki zadoščajo za", f"{meseci_varnosti_bolezen} mesecev")
        st.caption(f"Pri mesečni vrzeli {vrzel_stroski_bolezen:,.0f} € do stroškov.")

with c3:
    st.error("💥 **Nezgoda (70%)**")
    st.write(f"Mesečni manjko: **-{manjko_nezgoda:,.0f} €**")
    if isinstance(meseci_varnosti_nezgoda, str):
        st.success("Prihranki niso ogroženi.")
    else:
        st.metric("Prihranki zadoščajo za", f"{meseci_varnosti_nezgoda} mesecev")
    st.subheader(f"🛡️ {nadomestilo_nezgoda:.2f} €/dan")
    st.caption("Potrebno dnevno nadomestilo (nezgoda)")

st.markdown("---")

# --- PRIKAZ 2: HUDA BOLEZEN & KAPITALNA ZAŠČITA ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("⚠️ Scenarij: Huda bolezen")
    st.write(f"Skupna finančna luknja v 3 letih:")
    st.title(f"{skupni_izpad_huda_bolezen:,.0f} €")
    
    # Vizualizacija izpada
    meseci = list(range(1, 37))
    prihodek_po_mesecih = [bolniska_bolezen]*24 + [mesecni_prihodek * 0.5]*12
    fig_hb = go.Figure()
    fig_hb.add_trace(go.Scatter(x=meseci, y=prihodek_po_mesecih, fill='tozeroy', name='Prihodek', line_color='red'))
    fig_hb.add_hline(y=mesecni_stroski, line_dash="dash", line_color="black", annotation_text="Meja preživetja")
    fig_hb.update_layout(height=280, margin=dict(t=20, b=20), yaxis_title="Mesečni prihodek (€)")
    st.plotly_chart(fig_hb, use_container_width=True)

with col_right:
    st.subheader("📊 Kapitalna zaščita")
    
    def narisi_graf(naslov, vrednost, barva):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = vrednost,
            title = {'text': naslov, 'font': {'size': 16}},
            gauge = {'axis': {'range': [0, potreba_invalidnost + 20000]}, 'bar': {'color': barva}}
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    st.plotly_chart(narisi_graf("Vrzel: SMRT (3x letna + dolg)", vrzel_smrt, "#31333F"), use_container_width=True)
    st.plotly_chart(narisi_graf("Vrzel: INVALIDNOST (6x letna + dolg)", vrzel_invalidnost, "#FF4B4B"), use_container_width=True)
