import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Fonction principale de l'application
def main():
    

    # Charger les données
    data = pd.read_csv('dataset.csv')

    # Sélectionnez les colonnes catégorielles
    categorical_columns = ['Taille_Bagages', 'Origine', 'Destination', 'Contenu_Declare', 'Antecedents_Juridiques', 'Frequence_Voyage', 'Destination_Sejour']

    # Créer le transformateur de colonnes avec OneHotEncoder pour les caractéristiques catégorielles
    column_transformer = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(), categorical_columns)
        ],
        remainder='passthrough'  # cela permet de garder les autres colonnes non transformées
    )
    # Appliquer la transformation sur le DataFrame
    df_encoded_sparse = column_transformer.fit_transform(data)

    # Convertir la matrice sparse en matrice dense
    df_encoded = pd.DataFrame(df_encoded_sparse.toarray(), columns=column_transformer.get_feature_names_out())

    # Séparer les caractéristiques et la cible
    X = df_encoded.drop('remainder__Validation', axis=1)  # Utilisez le nom de la colonne correct après l'encodage
    y = df_encoded['remainder__Validation']  # Utilisez le nom de la colonne correct après l'encodage

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer et entraîner le modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Prédire les résultats sur l'ensemble de test
    y_pred = model.predict(X_test)

    # Créer un DataFrame contenant à la fois les données de test et les prédictions
    results = pd.DataFrame({'Validation_Predite': y_pred}, index=X_test.index)

    # Joindre les résultats avec le DataFrame original pour obtenir les caractéristiques correspondantes
    merged_df = data.join(results)

    # Filtrer les lignes où la prédiction est égale à 0
    predicted_zero = merged_df[merged_df['Validation_Predite'] == 0]
    final_data = predicted_zero.drop('Validation', axis=1)  # Supprimer la colonne 'Validation'

    # Titre pour la section de résultats
    st.subheader("Résultats de la prédiction")
    st.write("les voyageurs suceptibles d'etre malhonnetes sont ")

    # Afficher les lignes
    st.write(final_data)

# Point d'entrée principal de l'application
if __name__ == "__main__":
    st.title("Détection de voyageurs  suspects")
    st.subheader("Télécharger le fichier test.csv")
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
    if uploaded_file is not None:
        main()