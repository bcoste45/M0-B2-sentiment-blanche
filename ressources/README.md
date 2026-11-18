# M0-B2 — Pack ressources
> Brief M0-B2 « Déployer une IA NLP packagée — sentiment FR chez Aubergine
> Hôtels ». Sentiment FR avec CamemBERT, orchestration `docker compose`,
> UI Streamlit, mapping 5★ → 3 classes.

## Organisation du brief
- **Séance 1** : tâches 1 à 4, en binôme (ou poste solo)
- **Entre les deux séances** : livrables individuels A à D, dans `rendu/<prenom>/`
- **Séance 2** : tâches 5 et 6, finitions

## Ce que tu trouves ici
| Fichier | Quand le mobiliser | Durée de lecture |
| --- | --- | --- |
| [`01_DockerCompose_essentiel.md`](./01_DockerCompose_essentiel.md) | Tâches 1, 2 (mise en route + analyse de la stack), Tâche 5 (volume `./logs`) ; règle de reconstruction `docker compose up --build` après chaque modification de code (tâches 3, 4, 5 et 6) | ~30 min |
| [`02_HuggingFace_Transformers_essentiel.md`](./02_HuggingFace_Transformers_essentiel.md) | Tâche 3 (implémenter `/predict` + mapping 5★→3) | ~35 min |
| [`03_Streamlit_essentiel.md`](./03_Streamlit_essentiel.md) | Tâche 4 (UI utilisateur) | ~25 min |
| [`04_API_Integration_essentiel.md`](./04_API_Integration_essentiel.md) | Tâche 4 (côté UI : httpx + gestion erreurs) | ~25 min |
| [`05_Loguru_essentiel.md`](./05_Loguru_essentiel.md) | Tâche 5 (journalisation) | ~30 min |
| [`06_Pytest_API_essentiel.md`](./06_Pytest_API_essentiel.md) | Tâche 6 (tests) | — |
| [`liens_officiels.md`](./liens_officiels.md) | Recherche méthodique à tout moment | — |

> 💡 Les mini-cours `05` et `06` reprennent les notions de M0-B1, avec des
> exercices écrits pour cette stack (`/predict`, `payload.texte`).
> Pour le Dockerfile, relis `02_Docker_essentiel.md` dans ton repo M0-B1.

> Tout s'exécute dans Docker : ce brief ne demande aucun environnement virtuel
> Python sur ta machine. Les exemples marqués « facultatif, hors conteneur »
> demandent un environnement Python local : tu peux les ignorer.

**Ressources legacy OPCO ATLAS** (compléments optionnels) : disponibles
**à la demande sur Discord** auprès de la formatrice. Pour M0-B2, la doc
Streamlit ATLAS (~1620 mots, plus détaillée que notre mini-cours)
complète utilement `03_Streamlit_essentiel.md`.

## Ordre suggéré de consultation
1. **Avant la séance 1** : lire le README à la racine + parcourir
   `01_DockerCompose_essentiel.md` (au moins la section « Pourquoi »).
   Lire la « Situation professionnelle » du brief sur Simplonline : facultatif.
2. **Pendant les séances** : ouvrir chaque mini-cours dans l'ordre des
   tâches (`01` pour le démarrage, `02` pour `/predict`, `03` + `04`
   pour l'UI, `05` pour les logs, `06` pour les tests).
3. **En travail individuel** : revenir sur les sections « Pièges fréquents »
   et « Symptôme → cause probable » quand tu débogues en autonomie.

## Squelette de code
Le squelette de code, ce sont les fichiers à la **racine de ce repo** (créé
via « Use this template » — cf. [`README.md`](../README.md) racine). La stack
tourne dès le clone via `docker compose up --build` (plusieurs minutes au
premier démarrage). 1 test pytest passe d'office, `/predict` renvoie 501
(stub à compléter).
