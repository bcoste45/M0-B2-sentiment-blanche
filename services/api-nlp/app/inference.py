"""Logique d'inférence pour la classification de sentiment.

Le modèle CamemBERT chargé sort des labels 5 étoiles
(`'1 star'`, `'2 stars'`, ..., `'5 stars'`). Le métier (Aubergine Hôtels)
veut 3 classes (`négatif`, `neutre`, `positif`).

→ Ton travail dans ce fichier :
   1. Implémenter `predict_sentiment()` (récupère les scores 5★ + applique ta règle).
   2. Implémenter `map_stars_to_sentiment()` (mapping 5★ → 3 classes).
   3. Écrire ta règle dans le commentaire `# DECISION:` ci-dessous AVANT de coder.

Le pipeline transformers est chargé une seule fois au démarrage, dans
`main.py` (lifespan), et stocké dans `state["pipeline"]`. Tu le récupères
en argument.
"""
from __future__ import annotations

# DECISION: 
#   Règle retenue : Symétrie
# 1-2 étoiles -> négatif / 3 -> neutre / 4-5 -> positif
#   Argument métier 1 : Certaines personnes ne mettront jamais 5 étoiles même si tout est parfait (ils mettraient 4.999999 si possible), il vaut donc mieux considérer 4 comme positif; de même pour le négatif.
#   Argument métier 2 : Avoir une symétrie permet d'avoir une balance entre les positifs et les négatifs, et ainsi de voir de quel côté elle penche.

import time
from typing import Any

from app.schemas import Sentiment, SentimentOut


def map_stars_to_sentiment(star_label: str) -> Sentiment:
    """Mappe un label 5 étoiles ('1 star', ..., '5 stars') en 3 classes métier.


    Ton travail : proposer **ton** mapping et **le justifier** dans le
    commentaire `# DECISION:` en haut de ce fichier, puis dans
    `rendu/<prenom>/ANALYSE.md` (coût d'un faux positif / faux négatif
    côté métier Aubergine Hôtels).

    Args:
        star_label: label produit par le modèle (ex: '4 stars').

    Returns:
        Sentiment 3 classes.

    Raises:
        ValueError: si `star_label` n'est pas dans le format attendu.
    """
    if star_label == '1 star' or star_label=='2 stars':
        return "négatif"
    elif star_label=='3 stars':
        return "neutre"
    elif star_label=='4 stars' or star_label=='5 stars':
        return "positif"
    else :
        raise ValueError("Le star_label '"+star_label+"' n'est pas dans le format attendu")
    


def predict_sentiment(pipeline: Any, text: str, model_name: str) -> SentimentOut:
    """Inférence de sentiment sur un texte FR.

    Args:
        pipeline: pipeline `transformers.pipeline("text-classification", ...)`
            chargé au démarrage de l'API.
        text: texte FR de la review.
        model_name: identifiant HF du modèle (passé pour traçabilité).

    Returns:
        SentimentOut avec sentiment 3 classes, scores 5★ bruts, et latence ms.
    """
    t0 = time.perf_counter()
    raw = pipeline(text)
    tps_inf = (time.perf_counter() - t0)*1000 #en ms

    scores_5_stars = {}
    sentiments = {"négatif":0,"neutre":0,"positif":0}
    for l in raw[0]:
        scores_5_stars[l['label']] = round(l['score'],5)
        sentiments[map_stars_to_sentiment(l['label'])] += round(l['score'],5)

    return SentimentOut(
        sentiment= max(sentiments, key=sentiments.get),
        scores_5_stars=scores_5_stars,
        model_name=model_name,
        latence_ms=tps_inf
    )
