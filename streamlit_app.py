
import streamlit as st
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

# Configuration
st.set_page_config(
    page_title="Contrôle Solustop",
    page_icon="📊",
    layout="wide"
)

# Fuseau horaire utilisé pour les saisies
PARIS = ZoneInfo("Europe/Paris")
maintenant = datetime.now(PARIS)

# Valeurs initiales des champs
if "date_debut" not in st.session_state:
    st.session_state.date_debut = maintenant.date()

if "heure_debut" not in st.session_state:
    st.session_state.heure_debut = maintenant.time().replace(
        second=0, microsecond=0
    )

if "date_fin" not in st.session_state:
    st.session_state.date_fin = maintenant.date()

if "heure_fin" not in st.session_state:
    st.session_state.heure_fin = maintenant.time().replace(
        second=0, microsecond=0
    )


# Action du bouton Actuel
def renseigner_maintenant():
    instant = datetime.now(PARIS)
    st.session_state.date_fin = instant.date()
    st.session_state.heure_fin = instant.time().replace(
        second=0, microsecond=0
    )


# Conversion en timestamp Unix UTC, en millisecondes
def convertir_timestamp(jour, heure):
    date_heure = datetime.combine(
        jour, heure
    ).replace(tzinfo=PARIS)

    timestamp_ms = int(date_heure.timestamp() * 1000)

    date_utc = date_heure.astimezone(ZoneInfo("UTC"))

    return timestamp_ms, date_utc.strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


# Interface
st.title("Contrôle de planification Solustop")

st.write(
    "Paramétrez la période à analyser. "
    "Les dates et heures saisies sont exprimées en heure française."
)

st.divider()

st.header("1. Période de recherche")

# Début
col_date_debut, col_heure_debut = st.columns(2)

with col_date_debut:
    st.date_input(
        "Date de début",
        key="date_debut",
        format="DD/MM/YYYY"
    )

with col_heure_debut:
    st.time_input(
        "Heure de début",
        key="heure_debut",
        step=60
    )

# Fin et bouton Actuel
col_date_fin, col_heure_fin, col_actuel = st.columns(
    [1, 1, 0.55],
    vertical_alignment="bottom"
)

with col_date_fin:
    st.date_input(
        "Date de fin",
        key="date_fin",
        format="DD/MM/YYYY"
    )

with col_heure_fin:
    st.time_input(
        "Heure de fin",
        key="heure_fin",
        step=60
    )

with col_actuel:
    st.button(
        "Actuel",
        on_click=renseigner_maintenant,
        use_container_width=True
    )

# Calcul des timestamps
ts_debut, utc_debut = convertir_timestamp(
    st.session_state.date_debut,
    st.session_state.heure_debut
)

ts_fin, utc_fin = convertir_timestamp(
    st.session_state.date_fin,
    st.session_state.heure_fin
)

st.subheader("Timestamps UTC")

st.caption(
    "Calcul automatique en lecture seule — "
    "timestamps Unix en millisecondes."
)

col_ts_debut, col_ts_fin = st.columns(2)

with col_ts_debut:
    st.text_input(
        "Début — timestamp UTC (ms)",
        value=str(ts_debut),
        disabled=True
    )
    st.caption(f"Date UTC : {utc_debut}")

with col_ts_fin:
    st.text_input(
        "Fin — timestamp UTC (ms)",
        value=str(ts_fin),
        disabled=True
    )
    st.caption(f"Date UTC : {utc_fin}")

if ts_fin < ts_debut:
    st.error(
        "La date et l'heure de fin doivent être "
        "postérieures ou égales au début."
    )

st.divider()

st.header("2. Données Solustop")

st.info(
    "La connexion à l'API Solustop sera ajoutée "
    "dans une prochaine étape."
)
