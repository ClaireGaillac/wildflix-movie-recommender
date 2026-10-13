# Application WildFlix : moteur de recommandation de films.
"""
L'utilisateur se connecte (credentials.yaml), choisit un film ; le modèle KNN (entraîné dans train_model.py) 
trouve les 5 plus proches voisins, affiches et fiches détaillées.
"""

import streamlit as st
import pandas as pd
import joblib
import base64
import yaml
from streamlit_authenticator import Authenticate
from bandeau import afficher_bandeau
from scipy.sparse import csr_matrix

# Mise en page large
st.set_page_config(layout="wide")

# Chemins
CLEAN_PATH = "data/processed/movies_clean.csv"
MODEL_PATH = "model/knn_reco.joblib"
MATRIX_PATH = "model/features_sparse.joblib"
CREDENTIALS_PATH = "credentials.yaml"

# 1. Chargements mis en cache : sans cache, Streamlit recharge tout à chaque interaction.
@st.cache_data
def charger_films():
    return pd.read_csv(CLEAN_PATH)

@st.cache_resource
def charger_matrice():
    return joblib.load(MATRIX_PATH)

@st.cache_resource
def charger_modele():
    return joblib.load(MODEL_PATH)

# 2. Authentification : comptes lus depuis credentials.yaml. NOTE : en production, les mots de passe seraient
# hachés (bcrypt) — voir README, pistes d'amélioration.
with open(CREDENTIALS_PATH) as f:
    config = yaml.safe_load(f)

authenticator = Authenticate(config["credentials"], config["cookie"]["name"], config["cookie"]["key"], 
                             config["cookie"]["expiry_days"])
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrects")

elif st.session_state["authentication_status"] is None:
    st.warning("Les champs username et mot de passe doivent être remplis")

else:  # utilisateur connecté : tout le site est indenté ici, sinon il s'affiche sans authentification
    authenticator.logout("Déconnexion")

    df_films = charger_films()
    matrice = charger_matrice()
    model = charger_modele()

    # Titre + année dans la liste (distingue les remakes)
    df_films["TitreAnnee"] = df_films["Title"] + " (" + df_films["Year"].astype(str) + ")"

    # 3. Bandeau hero + son de démarrage
    afficher_bandeau()

    def autoplay_audio(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f'<audio autoplay><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>',
            unsafe_allow_html=True,
        )

    autoplay_audio("Netflix.mp3")

    # 4. Choix du film et fiche détaillée
    film_choisi = st.selectbox( "Indique le film dont tu veux recevoir des recommandations", 
                               sorted(df_films["TitreAnnee"].unique()))
    id_film = df_films.loc[df_films["TitreAnnee"] == film_choisi, "ID"].values[0]
    info = df_films.loc[df_films["ID"] == id_film].iloc[0]

    col1, col2 = st.columns([1, 3], vertical_alignment="center")
    with col1:
        st.image(info["Poster"])
    with col2:
        st.write(f"📖 Résumé : {info['Plot']}")
        st.write(f"🎞️ Genre : {info['Genre']}")
        st.write(f"📅 Année : {info['Year']}")
        st.write(f"⏳ Durée : {info['Runtime']} min")
        st.write(f"🎭 Acteurs : {info['Actors']}")
        st.write(f"🎬 Réalisateur : {info['Director']}")
        st.write(f"⭐ Note : {info['imdbRating']}/10")
        st.write(f"🔞 Rated : {info['Rated']}")

    # Infos secondaires pliées par défaut : interface épurée, le détail reste accessible en un clic
    with st.expander("🏆 Récompenses et box-office"):
        if pd.notna(info["Awards"]):
            st.write(f"🏆 Récompenses : {info['Awards']}")
        else:
            st.write("🏆 Récompenses : non")
        if pd.notna(info["BoxOffice"]):
            st.write(f"💰 Box-office : {info['BoxOffice']}")
        else:
            st.write("💰 Box-office : non renseigné")
        if pd.notna(info["Metascore"]):
            st.write(f"📰 Metascore : {info['Metascore']}/100")
        else:
            st.write("📰 Metascore : non renseigné")

    # 5. Recommandations : les 6 voisins les plus proches, puisque le premier est lui même
    index_film = df_films.index[df_films["ID"] == id_film][0]
    vecteur_film = csr_matrix(matrice[index_film])
    distances, indices = model.kneighbors(vecteur_film, n_neighbors=6)
    indices_reco = indices[0][1:]      # [1:] : on commence à 1 car le 1er voisin est le film lui-même
    distances_reco = distances[0][1:] 

    # DataFrame des voisins avec leur distance
    voisins = df_films.loc[indices_reco, ["Title"]].copy()
    voisins["distance"] = distances_reco
    voisins["indice"] = indices_reco

    st.subheader(f"Comme tu as aimé {film_choisi}, je te recommande :")
    tabs = st.tabs(voisins["Title"].tolist())

    # CSS : grossit le texte des onglets
    st.markdown("""<style>button[data-baseweb="tab"] p {font-size: 18px !important;}</style>""",
                unsafe_allow_html=True)

    for tab, (_, ligne) in zip(tabs, voisins.iterrows()):
        reco = df_films.loc[ligne["indice"]]
        with tab:
            c1, c2 = st.columns([1, 3], vertical_alignment="center")
            with c1:
                st.image(reco["Poster"])
            with c2:
                st.write(f"📖 Résumé : {reco['Plot']}")
                st.write(f"🎞️ Genre : {reco['Genre']}")
                st.write(f"📅 Année : {reco['Year']}")
                st.write(f"⏳ Durée : {reco['Runtime']} min")
                st.write(f"🎭 Acteurs : {reco['Actors']}")
                st.write(f"🎬 Réalisateur : {reco['Director']}")
                st.write(f"⭐ Note : {reco['imdbRating']}/10")
                st.write(f"🔞 Rated : {reco['Rated']}")
                # La distance cosinus : plus elle est proche de 0, plus le film est proche du film choisi 
                # (0 = identique). Il explique la recommandation.
                st.write(f"🎯 Distance avec ton film : {ligne['distance']:.3f} (0 = identique)")