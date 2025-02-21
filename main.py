import streamlit as st
import cv2
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()
# Configuration de l'API Gemini
apikey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apikey)
model = genai.GenerativeModel("gemini-2.0-flash")

# Fonction pour capturer une image
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        return image_path
    return None

# Fonction pour analyser l'image avec Gemini
def analyze_image(image_path):
    image = Image.open(image_path)
    prompt = "Analyse cette image en français et retourne la reponse en français faisant une reconnaissance faciale et détecte tout comportement suspect ou anormal en donnant tout les details."
    
    response = model.generate_content([prompt, image])
    return response.text if response else "Aucune analyse disponible."

# Interface Streamlit
st.title("Surveillance IA - Détection de comportements suspects")

# Initialiser session_state
if "image_path" not in st.session_state:
    st.session_state.image_path = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Bouton pour capturer une image
if st.button("Capturer une image", type="primary"):
    image_path = capture_image()
    if image_path:
        st.session_state.image_path = image_path  # Stocker l’image capturée

# Afficher l’image capturée si elle existe
if st.session_state.image_path:
    st.image(st.session_state.image_path, caption="Image capturée", use_container_width=True)

    # Bouton pour analyser l’image
    if st.button("Analyser", type="primary"):
        with st.spinner("Analyse en cours..."):
            result = analyze_image(st.session_state.image_path)
            st.session_state.analysis_result = result  # Stocker le résultat de l’analyse

# Afficher le résultat de l’analyse
if st.session_state.analysis_result:
    st.success("Analyse terminée")
    st.write(st.session_state.analysis_result)
        
