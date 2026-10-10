# Étape 1 de la pipeline WildFlix : fusion des données.
"""
Part de movies_raw.csv pour extraire les ID IMDb depuis les liens. Explique la création de movies_api.csv, 
mais pour ne pas refaire les appels API, utilise directement movies_api.csv crée en formation. Fusionne avec 
les données enrichies via l'API OMDb, et filtre sur les films uniquement et exporte le résultat dans 
movies_merged.csv.
"""

import pandas as pd
import requests

# Chemins
RAW_PATH = "data/raw/movies_raw.csv"
API_PATH = "data/api/movies_api.csv"
MERGED_PATH = "data/api/movies_merged.csv"

# Clé API OMDb (gratuite, obtenue sur omdbapi.com)
API_KEY = "votre_cle_api"

# 1. Chargement du dataset de base
df_raw = pd.read_csv(RAW_PATH)
print(f"Dataset brut : {df_raw.shape[0]} films")

# 2. Nettoyage des titres
df_raw["movie_title"] = df_raw["movie_title"].str.strip()

# Extrait l'ID IMDb (ex: tt0499549) d'un lien type : http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1
def extraire_id_imdb(lien):
    return (lien.replace("http://www.imdb.com/title/", "").replace("/?ref_=fn_tt_tt_1", "").strip())

# 3. Création de la colonne ID à partir des liens IMDb
df_raw["ID"] = df_raw["movie_imdb_link"].apply(extraire_id_imdb)

"""
Les 5043 films du dataset ont été répartis en 6 tranches de 1000 max, car c'est le plafond gratuit, pour 
répartir le temps d'appel entre les membres de l'équipe. Chaque tranche a été exportée puis les 6 fichiers 
ont été concaténés.

Répartition (à partir des liens IMDb du dataset brut) :

liste_id_1 = df_raw["ID"].iloc[:1000].tolist()      # 1 à 1000
liste_id_2 = df_raw["ID"].iloc[1000:2000].tolist()  # 1001 à 2000
liste_id_3 = df_raw["ID"].iloc[2000:3000].tolist()  # 2001 à 3000
liste_id_4 = df_raw["ID"].iloc[3000:4000].tolist()  # 3001 à 4000
liste_id_5 = df_raw["ID"].iloc[4000:5000].tolist()  # 4001 à 5000
liste_id_6 = df_raw["ID"].iloc[5000:].tolist()      # 5001 à 5043

Appelle l'API OMDb pour une liste d'ID de films et renvoie un DataFrame. Méthode utilisée en formation :
chaque membre de l'équipe a appelé l'API sur sa tranche, puis les résultats ont été concaténés dans 
movies_api.csv. Le fichier est acquis : cette fonction n'est plus exécutée, elle documente la façon dont 
les données ont été obtenues.

def extraire_donnees_api(liste_id):
    resultats = []
    for film_id in liste_id:
        reponse = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&i={film_id}").json()
        resultats.append(reponse)
    return pd.DataFrame(resultats)

Concaténation des 6 fichiers :
def reconstituer_movies_api():
    movies_api = pd.concat([resultats_1, resultats_2, resultats_3, resultats_4, resultats_5, resultats_6], 
                 ignore_index=True)
    return movies_api
"""

# 4. Chargement des données enrichies via l'API OMDb
df_api = pd.read_csv(API_PATH)
# Unnamed: 0 : index parasite créé lors de la concaténation des 6 extractions (chaque partie avait été 
# exportée avec son index, puis empilées en colonne)
df_api = df_api.drop(columns="Unnamed: 0")
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