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

# DECISION: (à écrire avant de coder, en français)
#   Règle retenue : ... étoiles -> négatif / ... -> neutre / ... -> positif
#   Argument métier 1 : ...
#   Argument métier 2 : ...

import time
from typing import Any

from app.schemas import Sentiment, SentimentOut


def map_stars_to_sentiment(star_label: str) -> Sentiment:
    """Mappe un label 5 étoiles ('1 star', ..., '5 stars') en 3 classes métier.

    À compléter par l'apprenant. **Le choix du mapping est un arbitrage
    métier**, pas une recette imposée : plusieurs découpages sont valides
    (cf. mini-cours `02_HuggingFace_Transformers_essentiel.md`, section
    "Justification du seuil de mapping").

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
    # TODO Tâche 3 — implémenter le mapping décrit dans `# DECISION:`.
    raise NotImplementedError("Compléter `map_stars_to_sentiment` (Tâche 3).")


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
    # TODO Tâche 3 — compléter :
    #
    # 1. Mesurer le temps d'inférence (time.perf_counter() avant/après).
    # 2. Appeler `raw = pipeline(text)` (sans argument en plus : le pipeline
    #    est déjà construit avec `top_k=None` dans `main.py`). `raw` est une
    #    liste contenant une liste de 5 dicts {'label', 'score'} : les
    #    probabilités sont dans `raw[0]`.
    # 3. Construire `scores_5_stars: dict[str, float]` à partir de `raw[0]`.
    # 4. Appliquer la règle écrite dans `# DECISION:` pour obtenir la classe
    #    métier : étoile la plus probable (puis `map_stars_to_sentiment`),
    #    ou somme des probabilités par groupe d'étoiles.
    # 5. Renvoyer un `SentimentOut(...)`.
    raise NotImplementedError("Compléter `predict_sentiment` (Tâche 3).")