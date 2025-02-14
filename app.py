import os
import streamlit as st
import pandas as pd
import plotly.express as px
from strategies.paroli_hybride import ParoliHybride

# Configuration des chemins pour Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PARIS_CSV = os.path.join(DATA_DIR, "paris.csv")
CAPITAL_JSON = os.path.join(DATA_DIR, "capital.json")

# Charger les données initiales
if "historique" not in st.session_state:
    st.session_state.historique = pd.read_csv(PARIS_CSV)
    with open(CAPITAL_JSON, "r") as f:
        st.session_state.capital_data = eval(f.read())
    st.session_state.strategie = ParoliHybride(st.session_state.capital_data["capital_initial"])

# Interface
st.title("📈 Paris Analytix - Stratégie Paroli Hybride")

cote = st.slider("Cote du pari", 1.3, 2.0, 1.5)
resultat = st.selectbox("Résultat", ["gain", "perte"])

if st.button("Valider le pari"):
    nouveau_capital = st.session_state.strategie.parier(cote, resultat)
    
    # Mettre à jour les données
    new_row = {
        "Date": pd.Timestamp.today().strftime("%Y-%m-%d"),
        "Cote": cote,
        "Resultat": resultat,
        "Mise": st.session_state.strategie.mise,
        "Capital_Avant": st.session_state.capital_data["historique"][-1],
        "Capital_Après": nouveau_capital
    }
    
    st.session_state.historique = st.session_state.historique.append(new_row, ignore_index=True)
    st.session_state.capital_data["historique"].append(nouveau_capital)
    
    # Sauvegarder (désactivé sur Streamlit Cloud)
    # st.session_state.historique.to_csv(PARIS_CSV, index=False)
    
    st.success(f"Capital mis à jour : {nouveau_capital} €")

# Afficher le graphique
fig = px.line(
    x=range(len(st.session_state.capital_data["historique"])),
    y=st.session_state.capital_data["historique"],
    labels={"x": "Nombre de paris", "y": "Capital (€)"},
    title="Évolution du Capital"
)
st.plotly_chart(fig)
