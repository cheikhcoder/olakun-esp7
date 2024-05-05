import streamlit as st
from PIL import Image

# Fonction pour charger une image
def load_image(image_path):
    img = Image.open(image_path)
    return img

# Fonction pour calculer le rang dans la liste
def calculate_rank():
    # Ici, vous pouvez implémenter la logique pour calculer le rang de l'utilisateur
    # Par exemple, vous pouvez récupérer la liste des réservations et déterminer où se situe l'utilisateur
    # Dans cette version, nous simulons juste un rang aléatoire
    return 15  # Rang aléatoire pour les besoins de la démonstration

# Page de réservation
def reservation():
    # Titre de la page
    st.title("Bienvenue dans votre application Olokun")
    st.write("Olokul vous aide à planifier votre passage à la douane de manière simple et pratique.")
    st.write("Réservez un créneau pour passer la douane et évitez les longues files d'attente.")

    # Formulaire de réservation
    st.subheader("Réserver un créneau à la douane")
    # Sélectionner le jour du vol
    selected_date = st.date_input("Sélectionnez le jour de votre vol")
    # Sélectionner l'heure du vol
    times = st.time_input("Sélectionnez l'heure de votre vol")
    selected_time = st.time_input("Sélectionneza laquelle vous voulez venir ")

    # Bouton de réservation
    if st.button("Réserver"):
        # Afficher un message de confirmation avec les détails de la réservation
        st.success(f"Votre créneau pour le {selected_date} à {selected_time} a été réservé avec succès!")

        # Calculer et afficher le rang dans la liste
        rank = calculate_rank()
        st.write(f"Votre rang dans la liste d'attente est : {rank}")

        # Vérifier si l'heure de réservation est optimale (pour l'exemple, nous supposons que toute heure est optimale)
        st.write("Votre heure de réservation est optimale.")

# Page d'accueil
def home():
    # Titre de la page

    # Charger l'image de fond
    # background_image = load_image("background_image.jpg")
    # st.image(background_image, use_column_width=True)

    # Informations de base
    
    

    # Formulaire de réservation
    reservation()

# Programme principal
def main():
    # Affichage de la page d'accueil
    home()

    # Section de vérification des documents
    st.subheader("Vérification des documents")
    # Formulaire pour télécharger les documents
    uploaded_visa = st.file_uploader("Téléchargez votre visa")
    uploaded_ticket = st.file_uploader("Téléchargez votre billet d'avion")
    uploaded_id = st.file_uploader("Téléchargez votre carte d'identité")

    # Vérifier si tous les documents ont été téléchargés
    if uploaded_visa and uploaded_ticket and uploaded_id:
        # Afficher un message de succès
        st.success("Tous les documents ont été téléchargés avec succès!")
    else:
        # Afficher un message d'avertissement s'il manque des documents
        st.warning("Veuillez télécharger tous les documents nécessaires.")

if __name__ == "__main__":
    main()
