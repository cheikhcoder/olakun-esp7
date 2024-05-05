import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialisez votre client OpenAI
client = OpenAI()

def main():
    st.title("Assistant Chatbot")
    st.write("""
Bienvenue à bord de notre chatbot d'assistant à la douane ! Conçu pour simplifier votre expérience de voyage, notre chatbot répond à vos questions sur les formalités douanières, vous guide à travers le processus de passage à la douane, et vous fournit des informations précises et utiles sur les documents requis, les restrictions d'importation et bien plus encore""")

    # Zone de texte pour que l'utilisateur saisisse son message
    user_input = st.text_area("Vous: ")

    if st.button("Envoyer"):
        # Appel à l'API OpenAI pour obtenir la réponse de l'assistant
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """Vous êtes un assistant chatbot conçu pour aider les voyageurs avec les formalités douanières. Vous devez fournir des informations sur les documents nécessaires, guider les voyageurs à travers le processus de passage à la douane, répondre à toute question liée aux procédures douanières et offrir une assistance générale pour faciliter leur voyage. Entrez vos questions concernant les documents requis, le processus de passage à la douane ou toute autre demande d'assistance douanière.
"""},
                {"role": "user", "content": user_input}
            ]
        )

        # Afficher la réponse de l'assistant
        assistant_response = completion.choices[0].message.content
        st.write("Assistant: ", assistant_response)

if __name__ == "__main__":
    main()
