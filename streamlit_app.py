
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Contrôle Solustop",
    page_icon="📊",
    layout="wide"
)

st.title("Contrôle de planification Solustop")

st.write(
    "Application de comparaison entre les données "
    "Solustop et le fichier de planification."
)

st.divider()

st.header("1. Importer le fichier de planification")

fichier = st.file_uploader(
    "Sélectionnez votre fichier Excel",
    type=["xlsx"]
)

if fichier is not None:
    try:
        planning = pd.read_excel(fichier)

        st.success("Fichier importé avec succès.")

        st.write("Nombre de lignes :", len(planning))
        st.write("Nombre de colonnes :", len(planning.columns))

        st.subheader("Aperçu du planning")

        st.dataframe(
            planning,
            use_container_width=True
        )

    except Exception as erreur:
        st.error(f"Impossible de lire le fichier : {erreur}")

st.divider()

st.header("2. Données Solustop")

st.info(
    "La connexion à l'API Solustop sera ajoutée "
    "dans une prochaine étape."
)
