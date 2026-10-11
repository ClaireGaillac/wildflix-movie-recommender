# Étape 3 de la pipeline WildFlix : création des features pour le machine learning.
"""
Part de movies_clean.csv, transforme les colonnes Genre, Actors et Director en colonnes binaires (une colonne
par genre / acteur / réalisateur : 1 si le film le contient, 0 sinon), puis exporte movies_features.csv, la 
matrice que consommera le modèle de recommandation.
"""

import pandas as pd

# Chemins
CLEAN_PATH = "data/processed/movies_clean.csv"
FEATURES_PATH = "data/features/movies_features.csv"

# 1. Chargement des données nettoyées
df_features = pd.read_csv(CLEAN_PATH)
print(f"Données nettoyées : {df_features.shape[0]} films")

# 2. Transformation de Genre
# "Action,Adventure,Sci-Fi" devient 3 colonnes (Action, Adventure, Sci-Fi) remplies de 0 et 1.
#  Etape par étape :
#   str.split(",", expand=True) -> sépare la colonne en plusieurs colonnes (une par élément)
#   .apply(lambda x: x.str.strip()) -> supprime les espaces autour de chaque valeur
#   .stack() -> empile toutes les valeurs en une seule colonne (en gardant le numéro du film)
#   pd.get_dummies(...) -> crée une colonne binaire par genre trouvé
#   .groupby(level=0).sum() -> regroupe par film : chaque film retrouve sa ligne, avec 1 dans chaque genre 
# qu'il contient
genres_split = df_features["Genre"].str.split(",", expand=True).apply(lambda x: x.str.strip())
genres_dummies = pd.get_dummies(genres_split.stack()).groupby(level=0).sum()
print(f"Genres : {genres_dummies.shape[1]} genres différents")

# 3. Transformation de Actors
actors_split = df_features["Actors"].str.split(",", expand=True).apply(lambda x: x.str.strip())
actors_dummies = pd.get_dummies(actors_split.stack()).groupby(level=0).sum()
print(f"Acteurs : {actors_dummies.shape[1]} acteurs différents")

# 4. Transformation de Director
director_split = df_features["Director"].str.split(",", expand=True).apply(lambda x: x.str.strip())
director_dummies = pd.get_dummies(director_split.stack()).groupby(level=0).sum()
print(f"Réalisateurs : {director_dummies.shape[1]} réalisateurs différents")

# 5. Concaténation : les colonnes d'origine + les colonnes binaires
df_features = pd.concat([df_features, genres_dummies, actors_dummies, director_dummies], axis=1)

# 6. Export de la matrice de features
df_features.to_csv(FEATURES_PATH, index=False)
print(f"Export : {FEATURES_PATH} ({df_features.shape[0]} films, {df_features.shape[1]} colonnes)")