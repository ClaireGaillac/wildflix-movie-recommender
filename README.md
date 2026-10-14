# 🎬 WildFlix — Système de recommandation de films

Application de recommandation de films basée sur le Machine Learning (KNN), construite à partir du dataset 
IMDB et enrichie par l'API OMDb.

**👉 Voir l'application en ligne** : https://wildflix-movie-recommender.streamlit.app/

## 🎯 Objectif

L'utilisateur choisit un film qu'il a aimé ; l'application lui recommande les 5 films les plus similaires 
selon leurs caractéristiques communes (genres, acteurs, réalisateur, scénariste).

## 🏗️ Architecture de la pipeline

```
data/raw/movies_raw.csv
    │
    ▼
extract_api.py      →    data/api/movies_merged.csv (enrichissement via API OMDb)
    ▼
clean_data.py       →    data/processed/movies_clean.csv (nettoyage, NaN, doublons)
    ▼
build_features.py   →    data/features/movies_features.csv (encodage binaire)
    ▼
train_model.py      →    model/knn_reco.joblib + features_sparse.joblib
    ▼
app.py              →    Application Streamlit (auth, bandeau, fiches, recommandations)
```

## 🧠 Le modèle : KNN en distance cosinus sur matrice creuse

- **Features** : genres, acteurs, réalisateur et scénariste, encodés en colonnes binaires (14 612 colonnes). La durée, l'année ou la note sont des données descriptives destinées à l'affichage : inclure une donnée
factuelle dans le modèle créerait des similarités sans sens cinéphile (un film n'est pas "similaire" à un autre pour sa durée).
- **Distance cosinus** : mesure la similarité indépendamment du volume de features.
- **Matrice creuse (scipy.sparse)** : la matrice 4808 × 14612 est presque entièrement composée de zéros. Stockée en format creux, la matrice pèse 510 Ko là où sa version dense (CSV) en fait 136 Mo et le rend déployable sur Streamlit Cloud.
- **algorithm="brute"** : en haute dimension, les structures arborescentes (KD-tree, Ball-tree) perdent leur intérêt ; la recherche exhaustive est le choix documenté pour données creuses + métrique cosinus. Son coût (4808 calculs de distance par requête) reste de l'ordre de quelques millisecondes.

## 🖥️ Fonctionnalités de l'application

- Authentification utilisateur (streamlit-authenticator, comptes en yaml)
- Bandeau hero animé 100 % CSS (caméra, faisceau, titre lettre par lettre)
- Sélection parmi 4 808 films (titre + année, pour distinguer les remakes)
- Fiche complète du film choisi : affiche, résumé, casting, note, récompenses et box-office
- 5 recommandations avec **distance cosinus affichée** : la transparence du modèle (plus la distance est proche de 0, plus les films sont similaires)

## ⚙️ Installation locale

```bash
git clone https://github.com/ClaireGaillac/wildflix-movie-recommender.git
cd wildflix-movie-recommender
python -m venv .venv
.venv\Scripts\activate        # Pour Windows
pip install -r requirements.txt
streamlit run src/app.py
```

Comptes de démonstration : `utilisateur / utilisateurMDP`

## 🔭 Pistes d'amélioration

- **Mots de passe hachés** : la démo stocke les comptes en clair dans credentials.yaml ; streamlit-authenticator supporte bcrypt pour la prod.
- **Filtrage collaboratif** : le modèle actuel est "content-based" ; permettre à l'utilisateur de noter les films et croiser ces notes permettrait des recos plus fines.
- **Traduction des résumés** : la traduction automatique gratuite (deep_translator / endpoint Google) s'est révélée non fiable (blocage IP selon l'environnement) ; une API officielle (DeepL) est la suite logique.
- **Ajouter les bandes annonces** : intégrer la bande-annonce de chaque film a été envisagé, mais les vidéos de promotion sont soumises aux droits des studios ; une source vidéo libre de droits serait la condition pour reprendre cette idée.