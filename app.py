import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prodajni Vizualizator: Varnostna Rezerva", layout="wide")

st.title("🛡️ Diagnostika finančne varnosti: Preživetveni model")
st.markdown("---")

# VNOSI V STRANSKI VRSTICI
with st.sidebar:
    st.header("👤 Finančni podatki")
    mesecni_prihodek = st.number_input("Mesečni neto prihodek (€)", value=2000, step=100)
    mesecni_stroski = st.number_input("Nujni mesečni stroški (€)", value=1700, step=100)
    
    st.markdown("---")
    kredit = st.number_input("Preostanek vseh kreditov (€)", value=80000, step=5000)
    prihranki = st.number_input("Trenutni prihranki (€)", value=5000)

# IZRAČUNI
# 1. Osnovna bolniška
bolniska_80 = mesecni_prihodek * 0.8
bolniska_90 = mesecni_prihodek * 0.9
bolniska_70_nezgoda = mesecni_prihodek * 0.7

# Mesečni manjko (Razlika med polno plačo in izplačilom)
manjko_bolezen_osnovno = mesecni_prihodek - bolniska_80
manjko_nezgoda = mesecni_prihodek - bolniska_70_nezgoda

# Dnevno nadomestilo samo za NEZGODO
nadomestilo_nezgoda = manjko_nezgoda / 30

# 2. Vzdržnost prihrankov (Primerjava z izpadom pri nezgodi)
def izracunaj_vzdrznost(prihranki, manjko):
    if manjko <= 0: return "Ni izpada"
    return round(prihranki / manjko, 1)

mesecev_prihrankov_nezgoda = izracunaj_vzdrznost(prihranki, manjko_nezgoda)

# 3. NOVI SCENARIJ: HUDA BOLEZEN (36 mesecev)
# - 3 mesece: 80% (izpad 20%)
# - 21 mesecev: 90% (izpad 10%)
# - 12 mesecev: 50% (izpad 50%)
izpad_huda_3m = (mesecni_prihodek * 0.2) * 3
izpad_huda_21m = (mesecni_prihodek * 0.1) * 21
izpad_huda_12m = (mesecni_prihodek * 0.5) * 12
skupni_izpad_huda_bolezen = izpad_huda_3m + izpad_huda_21m + izpad_huda_12m

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
    st.info("📌 **Vaša situacija**")
    st.write(f"Mesečna neto plača: **{mesecni_prihodek:,.0f} €**")
    st.write(f"Razpoložljivi prihranki: **{prihranki:,.0f} €**")
    st.write(f"Nujni mesečni stroški: **{mesecni_stroski:,.0f} €**")

with c2:
    st.warning("🤒 **Bolezen (Prvi meseci)**")
    st.write(f"Izpad dohodka (80%): **-{manjko_bolezen_osnovno:,.0f} €**")
    st.write(f"Kasneje (90%): **-{mesecni_prihodek*0.1:,.0f} €**")

with c3:
    st.error("💥 **Nezgoda (70% izplačilo)**")
    st.write(f"Mesečni izpad: **-{manjko_nezgoda:,.0f} €**")
    st.metric("Prihranki pokrijejo izpad za", f"{mesecev_prihrankov_nezgoda} mesecev")
    st.markdown(f"**Potrebno nadomestilo: {nadomestilo_nezgoda:.2f} €/dan**")

st.markdown("---")

# --- PRIKAZ 2: HUDA BOLEZEN (Specifična časovnica) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("⚠️ Scenarij: Huda bolezen (36 mesecev)")
    st.write("Potek izplačil:")
    st.markdown(f"1. **Mesec 1-3:** 80% ({bolniska_80:,.0f} €)")
    st.markdown(f"2. **Mesec 4-24:** 90% ({bolniska_90:,.0f} €)")
    st.markdown(f"3. **Mesec 25-36:** 50% ({mesecni_prihodek*0.5:,.0f} €)")
    
    st.metric("Skupni primanjkljaj v 3 letih", f"{skupni_izpad_huda_bolezen:,.0f} €")
    
    # Vizualizacija izpada po tvojem scenariju
    meseci = list(range(1, 37))
    prihodek_po_mesecih = [bolniska_80]*3 + [bolniska_90]*21 + [mesecni_prihodek * 0.5]*12
    
    fig_hb = go.Figure()
    fig_hb.add_trace(go.Scatter(x=meseci, y=prihodek_po_mesecih, fill='tozeroy', name='Prihodek', line_color='red', line_shape='hv'))
    fig_hb.add_hline(y=mesecni_stroski, line_dash="dash", line_color="black", annotation_text="Nujni stroški")
    fig_hb.update_layout(height=300, margin=dict(t=20, b=20), yaxis_title="Mesečni neto prihodek (€)", xaxis_title="Mesec rehabilitacije")
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

st.markdown("---")
st.success(f"💡 **Prodajni argument:** Kljub temu, da je bolniška sprva 90%, v zadnjem letu rehabilitacije prihodek pade globoko pod nujne stroške ({mesecni_stroski} €). Skupna luknja {skupni_izpad_huda_bolezen:,.0f} € je tista, ki jo mora pokriti polica za hude bolezni.")
