# Étape 2 de la pipeline WildFlix : nettoyage des données.
"""
Part de movies_merged.csv, supprime les colonnes inutiles et les doublons, nettoie les colonnes Language, 
Runtime, Rated et Color, puis exporte movies_clean.csv et movies_dashboard.csv (données pour le dashboard 
Power BI).
"""

import pandas as pd

# Chemins
MERGED_PATH = "data/api/movies_merged.csv"
CLEAN_PATH = "data/processed/movies_clean.csv"
DASHBOARD_PATH = "data/processed/movies_dashboard.csv"

# 1. Chargement des données fusionnées
df_clean = pd.read_csv(MERGED_PATH)
print(f"Données fusionnées : {df_clean.shape[0]} films, {df_clean.shape[1]} colonnes")

# 2. Suppression des colonnes inutiles. Les colonnes liées aux réseaux sociaux ne sont pas nécessaires à 
# notre analyse et ne font pas partie des variables explicatives : nous les avons donc retirées. Nous avons 
# conservé la note, mais pas le nombre de votes. La présence d'un DVD ou d'un site web n'étant pas 
# pertinente, ces colonnes ont également été supprimées. Enfin, nous avons retiré les colonnes relatives aux 
# autres types (séries, jeux vidéo), ainsi que la colonne Type elle-même, devenue inutile.
colonnes_inutiles = [
    "num_critic_for_reviews", "director_facebook_likes", "actor_3_facebook_likes","actor_1_facebook_likes", 
    "cast_total_facebook_likes", "facenumber_in_poster", "actor_2_facebook_likes", "aspect_ratio", 
    "movie_facebook_likes", "Released", "Ratings", "imdbID", "Type", "DVD", "Production", "Website", 
    "Response", "Season", "Episode", "seriesID", "totalSeasons",
]
df_clean = df_clean.drop(columns=colonnes_inutiles)
print(f"Après suppression des colonnes inutiles : {df_clean.shape[1]} colonnes")
print(df_clean.info())

# 3. Suppression des colonnes IMDb en doublon avec l'API (contenu parfaitement identique aux versions OMDb 
# après exploration)
colonnes_doublons_imdb = [
    "director_name", "duration", "actor_2_name", "gross", "genres", "actor_1_name", "movie_title", 
    "num_voted_users", "actor_3_name", "plot_keywords", "movie_imdb_link", "num_user_for_reviews", 
    "language", "country", "content_rating", "budget", "title_year", "imdb_score", "imdbVotes",
    "Year",   # on garde "year" (numérique, créé par l'équipe à partir de title_year)
]
df_clean = df_clean.drop(columns=colonnes_doublons_imdb)
print(f"Après suppression des doublons IMDb : {df_clean.shape[1]} colonnes")

# 4. Colonne Language : valeurs manquantes recherché pour corriger à la main.
df_clean.loc[df_clean["ID"] == "tt0785025", "Language"] = "English"
df_clean.loc[df_clean["ID"] == "tt1604100", "Language"] = "English"
df_clean.loc[df_clean["ID"] == "tt0770802", "Language"] = "No language"
df_clean.loc[df_clean["ID"] == "tt0067580", "Language"] = "English"

# 5. Colonne Runtime : suppression des " min" et conversion en nombre
df_clean["Runtime"] = df_clean["Runtime"].str.replace(" min", "", regex=False)
df_clean["Runtime"] = df_clean["Runtime"].astype("float32")

# Les 2 durées manquantes, recherché pour les ajouter à la main.
df_clean.loc[df_clean["ID"] == "tt0381053", "Runtime"] = 85
df_clean.loc[df_clean["ID"] == "tt1717210", "Runtime"] = 90

# Suppression du film avec un Runtime de 25 min (c'est un court métrage).
df_clean = df_clean[df_clean["Runtime"] != 25.0]

# 6. Colonne Rated : les mentions de la MPAA (États-Unis) ne sont pas lisibles par un public français, et 
# certaines sont désuètes (M, GP, Passed...). On les regroupe en familles claires. PG-13 et NC-17 sont 
# conservées : la forme "-13"/"-17" parle d'elle-même. M (1968) : "Mature, discrétion parentale conseillée" :
# renommé GP en 1970 puis PG en 1972 à cause de la confusion sur son sens. D'où son classement dans la 
# famille "accompagnement".
df_clean.loc[df_clean["Rated"] == "Passed", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "Approved", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "Not Rated", "Rated"] = "Non évalué"
df_clean.loc[df_clean["Rated"] == "Unrated", "Rated"] = "Non évalué"
df_clean.loc[df_clean["Rated"] == "TV-MA", "Rated"] = "NC-17"
df_clean.loc[df_clean["Rated"] == "M", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "TV-14", "Rated"] = "PG-13"
df_clean.loc[df_clean["Rated"] == "TV-PG", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "TV-G", "Rated"] = "Tous publics"
df_clean.loc[df_clean["Rated"] == "M/PG", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "GP", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "PG", "Rated"] = "Accompagnement parental conseillé"
df_clean.loc[df_clean["Rated"] == "G", "Rated"] = "Tous publics"
df_clean.loc[df_clean["Rated"] == "R", "Rated"] = "-17 (sauf accompagnement d'un adulte)"

print(df_clean["Rated"].value_counts())

# 7. Colonne Color : après recheche remplissage des vides
df_clean["color"] = df_clean["color"].fillna("Color")

# 8. Remplissage des dernières valeurs vides
df_clean["Rated"] = df_clean["Rated"].fillna("Non évalué")
df_clean["Actors"] = df_clean["Actors"].fillna("Non actors")

# 9. Vérification : où reste-t-il des valeurs vides ?
vides_restantes = df_clean.isna().sum()
print(f"Valeurs vides restantes : {vides_restantes[vides_restantes > 0]}")

# 10. Export des données nettoyées
df_clean.to_csv(CLEAN_PATH, index=False)
print(f"Export : {CLEAN_PATH} ({df_clean.shape[0]} films)")

# 11. Export pour le dashboard Power BI
df_clean.to_csv(DASHBOARD_PATH, index=False)
print(f"Export : {DASHBOARD_PATH}")