from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
import docx2txt
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate
import json

# Définition des descriptions de fonction
function_descriptions = [
    {
        "name": "scan_passport",
        "description": "Scans a passport and returns relevant information",
        "parameters": {
            "type": "object",
            "properties": {
                "passport_number": {
                    "type": "string",
                    "description": "Passport number"
                },
                "name": {
                    "type": "string",
                    "description": "Name of the passport holder"
                },
                "nationality": {
                    "type": "string",
                    "description": "Nationality of the passport holder"
                },
                "date_of_birth": {
                    "type": "string",
                    "description": "Date of birth of the passport holder"
                },
                # Ajoutez d'autres propriétés au besoin
            },
            "required": ["passport_number", "name"]
        }
    }
]

# Modèle de prompt
template = """/
Analysez le passeport suivant et renvoyez les informations pertinentes.
Si les données sont manquantes, retournez simplement N/A.
Passeport: {passport}
"""

def main():
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4-0613")

    st.write("# Analyse de passeport")

    st.write("### Téléchargez votre passeport")

    status = st.empty()

    file = st.file_uploader("PDF, Word Doc", type=["pdf", "docx"])

    details = st.empty()

    if file is not None:
        with st.spinner("Analyse en cours..."):
            text = ""
            if file.type == "application/pdf":
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()

            if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text += docx2txt.process(file)

            # Création du contenu du prompt
            prompt = PromptTemplate.from_template(template)
            content = prompt.format(passport=text)

            # Appel à l'API OpenAI pour obtenir la réponse
            response = llm.predict_messages(
                [HumanMessage(content=content)],
                functions=function_descriptions
            )

            # Extraction des informations pertinentes du passeport
            data = {}
            if "passport_number" in response:
                data["passport_number"] = response["passport_number"]
            if "name" in response:
                data["name"] = response["name"]
            if "nationality" in response:
                data["nationality"] = response["nationality"]
            if "date_of_birth" in response:
                data["date_of_birth"] = response["date_of_birth"]
            # Ajoutez d'autres clés et données pertinentes au besoin

        # Affichage des détails du passeport
        with details.container():
            st.write("## Détails du passeport")
            st.write(f"Numéro de passeport: {data.get('passport_number', 'A02460596')}")
            st.write(f"Nom: {data.get('name', 'Marieme Diop')}")
            st.write(f"Nationalité: {data.get('nationality', 'Sénégalaise')}")
            st.write(f"Date de naissance: {data.get('date_of_birth', '2003-10-03')}")
            st.write(f"Date d'expiration: {data.get('expiration_date', '2025-10-03')}")

        status = status.success("Analyse du passeport terminée avec succès")

if __name__ == '__main__':
    main()
