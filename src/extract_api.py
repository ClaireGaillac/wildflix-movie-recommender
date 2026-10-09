# Étape 1 de la pipeline WildFlix : fusion des données.
"""
Part du dataset de base (movies_raw.csv), extrait les ID IMDb depuis les liens, fusionne avec les données 
enrichies via l'API OMDb (movies_api.csv), filtre sur les films uniquement et exporte le résultat dans 
movies_merged.csv.
"""

import pandas as pd

# Chemins
RAW_PATH = "data/raw/movies_raw.csv"
API_PATH = "data/api/movies_api.csv"
MERGED_PATH = "data/api/movies_merged.csv"

# Extrait l'ID IMDb (ex: tt0499549) d'un lien type : http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1
def extraire_id_imdb(lien):
    return (lien.replace("http://www.imdb.com/title/", "").replace("/?ref_=fn_tt_tt_1", "").strip())


# 1. Chargement du dataset de base
df_raw = pd.read_csv(RAW_PATH)
print(f"Dataset brut : {df_raw.shape[0]} films")

# 2. Nettoyage des titres
df_raw["movie_title"] = df_raw["movie_title"].str.strip()

# 3. Création de la colonne ID à partir des liens IMDb
df_raw["ID"] = df_raw["movie_imdb_link"].apply(extraire_id_imdb)

# 4. Chargement des données enrichies via l'API OMDb
df_api = pd.read_csv(API_PATH)
print(f"Données API : {df_api.shape[0]} entrées")

# 5. Jointure : on ne garde que les films présents dans les deux sources
df_merged = pd.merge(df_raw, df_api, how="inner", left_on="ID", right_on="imdbID")

# 6. Suppression des doublons
df_merged = df_merged.drop_duplicates(subset="ID")

# 7. Filtre : garder uniquement les films (exclut séries, jeux vidéo...)
df_merged = df_merged.loc[df_merged["Type"] == "movie"]
print(f"Après filtre 'film uniquement' : {df_merged.shape[0]} films")

# 8. Export (index=False : évite la colonne "Unnamed: 0")
df_merged.to_csv(MERGED_PATH, index=False)
print(f"Export : {MERGED_PATH}")