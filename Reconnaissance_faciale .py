import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model


def main():
    st.title("Prédiction à partir d'une image")

    # Charger le modèle Keras
    model = load_model("keras_model.h5", compile=False)

    # Charger les noms de classes à partir du fichier labels.txt
    with open("labels.txt", "r") as f:
        class_names = f.readlines()

    # Créer le tableau de la forme appropriée pour alimenter le modèle Keras
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Télécharger une image depuis l'utilisateur
    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])

    # Si une image est téléchargée
    if uploaded_file is not None:
        # Afficher l'image
        image = Image.open(uploaded_file)
        st.image(image, caption="Image téléchargée", use_column_width=True)

        # Prétraitement de l'image
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        # Prédiction
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index].strip()
        confidence_score = prediction[0][index]
        # Liste des noms enregistrés par fichiers
        noms_registres = ["SEYDOU KA",  "Mame Fatou Sarr", "Cheikh Tidiane Dieng"]
        noms_docs_voles = ["Cheikh Tidiane Dieng", "Raky", "Mouhamed Ndiaye"]
        donnees_biometriques = ["Mareme Diop", "Mame Fatou Sarr", "Djiba"]

        class_name_ = class_name[2:].strip().lower()
        noms_carceral_ = [nom.strip().lower() for nom in noms_registres]

        # Afficher la prédiction
        if confidence_score < 0.65:
            st.write(" La personne n'a pas été reconnue")
        else:
            st.write(f"Personne sur la photo : {class_name}")
            st.write(f"Score de confiance : {confidence_score*100} %")
        
        # Vérifier dans la liste des noms dans les donnees carcéraux
        if class_name_ in noms_carceral_ :
            st.write("Il se trouve dans le registre des données carcéraux")
        else:
            st.write("Pas de casier")
            
        # Verification dans les documents voles 
        # if class_name_ in noms_docs_voles :
        #     st.write("DANS LE REGISTRE DES DOCUMENTS VOLES")
        # else:
        #     st.write("Document conforme pas volé")
        
        # Verification dans les donnees_biometriques 
        if class_name_ in donnees_biometriques:
            st.write(" Il se trouve dans le registre des données biométriques")
        else:
            st.write("Pas dans la base des documents biométriques")

if __name__ == '__main__':
    main()