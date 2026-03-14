import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Analiza finančne vrzeli", layout="wide")

# Naslov in uvod
st.title("🛡️ Diagnostika družinske finančne varnosti")
st.markdown("---")

# Glavna postavitev: Levi del za vnose, desni za rezultat
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.header("📋 Vhodni podatki")
    
    with st.expander("Stroški in dolgovi", expanded=True):
        mesecni_stroski = st.slider("Mesečni proračun družine (€)", 800, 10000, 2000, step=100)
        leta_podpore = st.number_input("Leta kritja (npr. do konca šolanja)", value=15)
        kredit = st.number_input("Preostali dolgovi/krediti (€)", value=80000)

    with st.expander("Viri in prihranki", expanded=True):
        prihranki = st.number_input("Trenutna likvidna sredstva (€)", value=10000)
        drzava = st.slider("Socialna varnost/Pokojnina (€/mesec)", 0, 1200, 550)

# Izračuni (Logika vrzeli)
potrebe_skupaj = (mesecni_stroski * 12 * leta_podpore) + kredit
viri_skupaj = (drzava * 12 * leta_podpore) + prihranki
vrzel = potrebe_skupaj - viri_skupaj

# Približna dnevna premija (informativno za prodajni argument)
dnevna_premija = (vrzel / 100000) * 0.80  # Okvirna ocena: 0.80€ na 100k kritja

with col2:
    st.header("📊 Vaša finančna slika")
    
    if vrzel > 0:
        # Vizualizacija z Grafom
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = vrzel,
            title = {"text": "Finančni primanjkljaj (GAP)"},
            number = {'suffix': " €", 'font': {'color': 'red'}},
            delta = {'reference': 0, 'relative': False}
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Primerjava s ceno kave (Visual Benchmarking)
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Vrednost vrzeli", f"{vrzel:,.0f} €")
            st.caption("Znesek, ki ga vaša družina nima v primeru izpada dohodka.")
        with c2:
            st.metric("Dnevna investicija", f"{dnevna_premija:.2f} €")
            st.caption("Cena za popolno zaprtje te vrzeli.")

        # PRODAJNI ARGUMENT S SLIKO/IKONO
        st.info(f"💡 **Primerjava:** Zaprtje te vrzeli vas stane manj kot **ena kava v mestu dnevno**. Ali je varnost vaše družine vredna 1.50 €?")
    else:
        st.success("Čestitamo! Vaša trenutna sredstva in državna kritja zadoščajo vašim ciljem.")

# Dodatek za Coache (Psihometrični nasvet)
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Coach kotiček (DISC)")
tip_stranke = st.sidebar.selectbox("Tip stranke:", ["D - Dominanten", "I - Interaktiven", "S - Stanoviten", "C - Analitičen"])

nasveti = {
    "D - Dominanten": "Fokusiraj se na 'Kontrolo'. Brez zavarovanja izgubijo nadzor nad svojo zapuščino.",
    "I - Interaktiven": "Fokusiraj se na 'Zgodbo'. Kako bo družina ohranila življenjski slog in status?",
    "S - Stanoviten": "Fokusiraj se na 'Varnost'. Poudari mirno spanje in zaščito najbližjih.",
    "C - Analitičen": "Fokusiraj se na 'Logiko'. Pokaži jim izračun vrzeli do zadnjega evra."
}
st.sidebar.write(nasveti[tip_stranke])
