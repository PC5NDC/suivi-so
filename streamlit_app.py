
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Contrôle de planification Solustop", layout="wide")
st.title("Contrôle de planification Solustop")

paris = ZoneInfo("Europe/Paris")

if "date_debut" not in st.session_state:
    st.session_state.date_debut = date(2026, 5, 23)
if "heure_debut" not in st.session_state:
    st.session_state.heure_debut = time(0, 0)
if "date_fin" not in st.session_state:
    st.session_state.date_fin = date(2026, 5, 25)
if "heure_fin" not in st.session_state:
    st.session_state.heure_fin = time(20, 0)

def afficher_actuel():
    maintenant = datetime.now(paris)
    st.session_state.date_fin = maintenant.date()
    st.session_state.heure_fin = maintenant.time().replace(second=0, microsecond=0)

st.subheader("Période de contrôle")
col1, col2 = st.columns(2)

with col1:
    st.date_input("Date de début", key="date_debut")
    st.time_input("Heure de début", key="heure_debut")

with col2:
    st.date_input("Date de fin", key="date_fin")
    st.time_input("Heure de fin", key="heure_fin")
    st.button("Actuel", on_click=afficher_actuel)

debut = datetime.combine(
    st.session_state.date_debut,
    st.session_state.heure_debut,
    tzinfo=paris,
)
fin = datetime.combine(
    st.session_state.date_fin,
    st.session_state.heure_fin,
    tzinfo=paris,
)

col1, col2 = st.columns(2)
with col1:
    st.caption("Timestamp UTC de début (ms)")
    st.code(str(int(debut.timestamp() * 1000)))
with col2:
    st.caption("Timestamp UTC de fin (ms)")
    st.code(str(int(fin.timestamp() * 1000)))

st.divider()
st.subheader("Import du fichier de planification")

fichier = st.file_uploader(
    "Sélectionnez une copie Excel (.xlsx ou .xlsm)",
    type=["xlsx", "xlsm"],
)

if fichier is not None:
    try:
        classeur = pd.ExcelFile(fichier)
        feuilles = classeur.sheet_names
        st.success(f"Fichier chargé : {fichier.name}")
        st.write(f"{len(feuilles)} feuilles détectées.")

        feuille = st.selectbox("Feuille à consulter", feuilles)
        donnees = pd.read_excel(classeur, sheet_name=feuille)
        st.write(f"{len(donnees)} lignes et {len(donnees.columns)} colonnes")
        st.dataframe(donnees, use_container_width=True)

    except Exception as e:
        st.error(f"Impossible de lire ce fichier : {e}")
