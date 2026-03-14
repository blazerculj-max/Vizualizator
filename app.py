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
    prihranki = st.number_input("Trenutna likvidna sredstva (€)", value=5000)

# IZRAČUNI
# 1. Bolniška: Bolezen (80%) vs Nezgoda (70%)
bolniska_bolezen = mesecni_prihodek * 0.8
bolniska_nezgoda = mesecni_prihodek * 0.7

# VRZEL glede na stroške (Koliko zmanjka za preživetje?)
vrzel_prezivetja_bolezen = mesecni_stroski - bolniska_bolezen
vrzel_prezivetja_nezgoda = mesecni_stroski - bolniska_nezgoda

# 2. Scenarij HUDA BOLEZEN (3-letni vpliv)
izpad_leto_1_2 = (mesecni_prihodek * 0.2) * 24 
izpad_leto_3 = (mesecni_prihodek * 0.5) * 12
skupni_izpad_huda_bolezen = izpad_leto_1_2 + izpad_leto_3

# 3. Formule za zavarovalne vsote
letni_prihodek = mesecni_prihodek * 12
potreba_smrt = (letni_prihodek * 3) + kredit
potreba_invalidnost = (letni_prihodek * 6) + kredit

vrzel_smrt = max(0, potreba_smrt - prihranki)
vrzel_invalidnost = max(0, potreba_invalidnost - prihranki)

# --- PRIKAZ 1: PREŽIVETVENI PRIMANJKLJAJ ---
st.subheader("📉 Ali vaša bolniška sploh pokrije nujne stroške?")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Nujni stroški", f"{mesecni_stroski:,.0f} €")
    st.caption("Vaš minimalni mesečni prag.")

with c2:
    delta_b = -vrzel_prezivetja_bolezen if vrzel_prezivetja_bolezen > 0 else abs(vrzel_prezivetja_bolezen)
    st.metric("Bolezen (80%)", f"{bolniska_bolezen:,.0f} €", delta=f"{delta_b:,.0f} €")
    if vrzel_prezivetja_bolezen > 0:
        st.error(f"Primanjkljaj za stroške: {vrzel_prezivetja_bolezen:,.0f} €")

with c3:
    delta_n = -vrzel_prezivetja_nezgoda if vrzel_prezivetja_nezgoda > 0 else abs(vrzel_prezivetja_nezgoda)
    st.metric("Nezgoda (70%)", f"{bolniska_nezgoda:,.0f} €", delta=f"{delta_n:,.0f} €")
    if vrzel_prezivetja_nezgoda > 0:
        st.error(f"Primanjkljaj za stroške: {vrzel_prezivetja_nezgoda:,.0f} €")

st.markdown("---")

# --- PRIKAZ 2: HUDA BOLEZEN & KAPITALNA ZAŠČITA ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("⚠️ Scenarij: Huda bolezen")
    st.write(f"V 3 letih bi vaši družini za preživetje in rehabilitacijo zmanjkalo:")
    st.title(f"{skupni_izpad_huda_bolezen:,.0f} €")
    
    # Vizualizacija izpada
    meseci = list(range(1, 37))
    prihodek_po_mesecih = [bolniska_bolezen]*24 + [mesecni_prihodek * 0.5]*12
    fig_hb = go.Figure()
    fig_hb.add_trace(go.Scatter(x=meseci, y=prihodek_po_mesecih, fill='tozeroy', name='Prihodek', line_color='red'))
    fig_hb.add_hline(y=mesecni_stroski, line_dash="dash", line_color="black", annotation_text="Nujni stroški")
    fig_hb.update_layout(height=250, margin=dict(t=20, b=20))
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

    st.plotly_chart(narisi_graf("Vrzel: SMRT", vrzel_smrt, "#31333F"), use_container_width=True)
    st.plotly_chart(narisi_graf("Vrzel: INVALIDNOST", vrzel_invalidnost, "#FF4B4B"), use_container_width=True)

st.info("💡 **Coach nasvet:** Ko stranka vidi, da črna črta (stroški) leži nad rdečim poljem (prihodek), vprašanje ni več 'ali potrebujem zavarovanje', ampak 'kako bomo preživeli'.")
