"""UI Streamlit pour le service NLP Aubergine Hôtels.

Au clone, l'UI s'affiche mais ne consomme PAS encore l'API. À toi de :

1. Implémenter l'appel à `POST /predict` via httpx (Tâche 4 du brief).
2. Gérer les erreurs (API down, timeout 10 s).
3. Afficher le sentiment avec une couleur selon la classe :
   - 🔴 négatif → couleur rouge
   - 🟠 neutre  → couleur orange
   - 🟢 positif → couleur verte
4. Afficher les probabilités 5 étoiles brutes en barres (st.bar_chart).

L'URL de l'API est dans la variable d'environnement `API_URL`
(injectée par docker-compose, vaut `http://api-nlp:8000`).
"""
from __future__ import annotations

import os

import streamlit as st
import httpx


API_URL: str = os.getenv("API_URL", "http://api-nlp:8000")


st.set_page_config(
    page_title="Aubergine Hôtels — sentiment FR",
    page_icon="🍆",
    layout="centered",
)

st.title("🍆 Aubergine Hôtels — qualification du sentiment")
st.caption(
    "Démo interne : copie une review FR, le service NLP renvoie son sentiment "
    "en 3 classes (négatif / neutre / positif)."
)

texte = st.text_area(
    "Texte de la review",
    height=150,
    placeholder="Ex : Personnel charmant, chambre impeccable, on reviendra !",
)

if st.button("Analyser", type="primary", disabled=not texte.strip()):
    
    try :
        with st.spinner("Analyse en cours…"): #Loader
            # Appel POST avec httpx
            response = httpx.post(f"{API_URL}/predict", json={"texte": texte}, timeout=10)
            response.raise_for_status()            
        # En cas d'erreur réseau ou HTTP >= 500 : affiche un message d'erreur clair via st.error("...").
    except httpx.TimeoutException:
        st.error("⏱️  Timeout : l'API a mis plus de 10 s.")
    except httpx.ConnectError:
        st.error("🔌 Connexion refusée : l'API tourne-t-elle ?")
    except httpx.HTTPStatusError as exc:
        st.error(f"❌ HTTP {exc.response.status_code} : {exc.response.text}")
    else:
        data = response.json()
        # Affiche le sentiment dans un encadré coloré (st.success / st.warning / st.error selon la classe).
        if data['sentiment'] == 'positif':
            st.success(f"Sentiment : {data['sentiment']}")
        elif data['sentiment'] == 'neutre':
            st.warning(f"Sentiment : {data['sentiment']}")
        else :            
            st.error(f"Sentiment : {data['sentiment']}")
        # Affiche les scores 5 étoiles bruts via st.bar_chart().
        st.bar_chart(data['scores_5_stars'],y_label='Probabilités')

        st.info(f"Latence : {data['latence_ms']} ms")

with st.sidebar:
    st.markdown(f"**API URL** : `{API_URL}`")
    st.markdown(
        "**Statut** : OK.\n\n"
        "L'UI affiche :\n"
        "- Le sentiment (3 classes)\n"
        "- Les probas 5★ brutes\n"
        "- Un message d'erreur clair si l'API tombe"
    )