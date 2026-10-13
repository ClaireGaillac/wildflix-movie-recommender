# Étape 4 de la pipeline WildFlix : entraînement du modèle de recommandation.
"""
Part de movies_features.csv, sélectionne les colonnes binaires (genres, acteurs, réalisateurs) et entraîne un
modèle KNN (voisinage cosinus) qui trouve les films les plus proches. Le modèle est sauvegardé dans 
model/knn_reco.joblib pour être utilisé par l'application Streamlit.
"""

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix   # format creux : ne stocke que les 1
import joblib

# Chemins
FEATURES_PATH = "data/features/movies_features.csv"
MODEL_PATH = "model/knn_reco.joblib"
MATRIX_PATH = "model/features_sparse.joblib"   # matrice creux pour l'app Streamlit

# 1. Chargement de la matrice de features
df_features = pd.read_csv(FEATURES_PATH)
print(f"Features chargées : {df_features.shape[0]} films, {df_features.shape[1]} colonnes")

# 2. Sélection des colonnes binaires : tout sauf les 17 colonnes de base
colonnes_base = ["ID", "Title", "Rated", "Runtime", "Genre", "Director", "Writer", "Actors", "Plot", 
                 "Language", "Country", "Awards", "Poster", "Metascore", "imdbRating", "BoxOffice", 
                 "color", "Year"]
X = df_features.drop(columns=colonnes_base)
print(f"Matrice pour le modèle : {X.shape[0]} films, {X.shape[1]} colonnes binaires")

# 3. Entraînement du KNN : le modèle apprend "qui est proche de qui" metric="cosine" : la distance entre 
# deux films est l'angle entre leurs vecteurs de 0 et 1 (deux films qui partagent beaucoup de 
# genres/acteurs/réalisateurs/scénaristes ont des vecteurs qui pointent dans la même direction)
X_sparse = csr_matrix(X.values)
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(X_sparse)
print("Modèle KNN entraîné")

# 4. Sauvegarde
joblib.dump(model, MODEL_PATH)
print(f"Export : {MODEL_PATH}")

joblib.dump(X_sparse, MATRIX_PATH)
print(f"Export : {MATRIX_PATH}")