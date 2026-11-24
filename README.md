# M0-B2 — Déployer une IA NLP packagée (sentiment FR chez Aubergine Hôtels)

La chaîne d'hôtels Aubergine Hôtels reçoit des avis, elle veut pouvoir classifier ces avis en 3 classes sentiment (négatif, neutren positif) afin de pouvoir analyser les négatifs et améliorer leur services.  
On utilise le modèle pré-entraîné camemBERT pour avoir une évaluation en étoiles des avis puis on la transforme en sentiment.  

---

## 🚀 Démarrage (4 étapes)

```bash
# 0. Clone le repo du binôme et crée ta branche
#    (la personne invitée accepte d'abord l'invitation reçue par mail ;
#     sans clé SSH, utilise l'adresse https://github.com/... du repo)
#    🧍 Poste solo : tu clones ton propre repo, il n'y a pas d'invitation.
git clone git@github.com:<user>/M0-B2-sentiment-<prenom1>-<prenom2>.git
cd M0-B2-sentiment-<prenom1>-<prenom2>
git switch -c <prenom>

# 1. Configurer l'environnement (Docker Desktop : au moins 6 Go de mémoire
#    alloués, sinon le conteneur de l'API est tué sans message)
cp .env.example .env

# 2. Construire et lancer la stack
docker compose up --build

# 3. Vérifier (dans un autre terminal)
curl http://localhost:8000/health        # API NLP
# UI Streamlit : ouvre http://localhost:8501 dans ton navigateur
```

À l'arrêt : `Ctrl+C` puis `docker compose down` (les volumes `models/` et
`logs/` sont conservés — le modèle HF n'est pas re-téléchargé au prochain `up`).

> ⏱️ Premier démarrage : plusieurs minutes (build puis téléchargement du
> modèle DistilCamemBERT, ~270 Mo). C'est normal, ce n'est pas une panne :
> suis l'avancement avec `docker compose logs -f api-nlp`. Les démarrages
> suivants : `api-nlp` passe `healthy` en moins d'une minute grâce au cache `models/`.

---
Pour voir les services Docker qui tournent et leur état de santé :
```bash
docker compose ps
NAME                IMAGE                                                                     COMMAND                  SERVICE        CREATED       STATUS                 PORTS
m0b2-api-nlp        m0-b2-sentiment-blanche-api-nlp                                           "uvicorn app.main:ap…"   api-nlp        3 hours ago   Up 3 hours (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
m0b2-ui-streamlit   sha256:b04eba1c08fee8606c10ff026ce4cdcb03fb9557a9344b31b459def7074780fc   "streamlit run app.p…"   ui-streamlit   5 hours ago   Up 5 hours             0.0.0.0:8501->8501/tcp, [::]:8501->8501/tcp``
```
*On voit ici que le service api-nlp a bien un status healthy*

## 🧠 Modèle utilisé

**`cmarkea/distilcamembert-base-sentiment`** — DistilCamemBERT FR, 68 M
paramètres, ~270 Mo.

⚠️ Le modèle sort **5 étoiles** (`'1 star'` … `'5 stars'`). 
Le métier (Aubergine Hôtels) veut **3 classes** (`négatif/neutre/positif`).
On adopte un mapping symétrique regroupé, ainsi 4-5 étoile = positif, 3 étoiles = neutre et 1-2 étoiles = négatif; on cumule les probabiltés par étoiles pour chaque sentiment. 


## 📁 Structure du repo

```
M0-B2-sentiment-<prenom1>-<prenom2>/
├── docker-compose.yml             ← 2 services + healthcheck api-nlp
├── .env.example
├── .env
├── services/
│   ├── api-nlp/                   ← FastAPI + transformers
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py            ← routes (lifespan + /health + /info + /predict)
│   │   │   ├── schemas.py         ← Pydantic ReviewIn / SentimentOut
│   │   │   └── inference.py       ← TON CODE + mapping 5→3
│   │   └── tests/
│   │       └── test_health.py     ← 1 test pytest qui passe 
│   │       └── test_predict.py    ← 7 tests pytest qui passent 
│   └── ui-streamlit/              ← UI utilisateur
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app.py                 ← UI à compléter (brancher l'appel HTTP)
├── data/
│   └── sample_reviews.csv         ← 30 reviews FR fictives (Aubergine Hôtels)
├── postman/
│   └── M0-B2_collection.json      ← point de départ de ta collection
├── rendu/
│   ├── ANALYSE.md             ← schéma Mermaid + reviews mal classées + mapping
│   └── postman_collection.json
├── ressources/                    ← 📚 mini-cours d'appui (lecture juste-à-temps)
│   ├── 01_DockerCompose_essentiel.md
│   ├── 02_HuggingFace_Transformers_essentiel.md
│   ├── 03_Streamlit_essentiel.md
│   ├── 04_API_Integration_essentiel.md
│   ├── 05_Loguru_essentiel.md
│   ├── 06_Pytest_API_essentiel.md
│   ├── liens_officiels.md
│   └── README.md
├── .gitignore
└── README.md (ce  fichier — à compléter : ajoutez en haut 5 à 10 lignes sur votre service et les 3 preuves ; gardez le reste)
```

---

## ✏️ Endpoints fournis

| Endpoint | Statut au clone | Ce que tu dois faire |
|---|---|---|
| `GET /health` | ✅ fonctionnel | rien |
| `GET /info` | ✅ fonctionnel | rien |
| `POST /predict` | ✅ fonctionnel | fournir un json avec du texte |

L'UI Streamlit est lancée mais affiche **« API non branchée »** tant que tu
n'as pas branché l'appel HTTP dans `services/ui-streamlit/app.py`.

---
```bash
curl -X 'GET' \
  'http://localhost:8000/health' \
  -H 'accept: */*'
```
Réponse :
```json
{
  "status": "ok",
  "model_loaded": true
}
```
---

```bash
curl -X 'GET' \
  'http://localhost:8000/info' \
  -H 'accept: */*Réponse :
```
Réponse :
```json
{
  "service": "FastIA Aubergine — sentiment FR",
  "model_name": "cmarkea/distilcamembert-base-sentiment",
  "native_classes": [
    "1 star",
    "2 stars",
    "3 stars",
    "4 stars",
    "5 stars"
  ],
  "target_classes": [
    "négatif",
    "neutre",
    "positif"
  ],
  "max_text_length": 2000
}
```
   ---

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "texte": "Personnel charmant, chambre impeccable !"
}'
```
Réponse :
```json
{
  "sentiment": "positif",
  "scores_5_stars": {
    "5 stars": 0.55489,
    "4 stars": 0.39403,
    "3 stars": 0.04447,
    "2 stars": 0.00493,
    "1 star": 0.00167
  },
  "model_name": "cmarkea/distilcamembert-base-sentiment",
  "latence_ms": 2147.801705999882
}
```

## ✅ Tests & environnement
L'api api-nlp a 7 tests pytests :
- un pour GET /heath qui doit retourner un code 200
- les autres pour POST /predict
  - un avis positif => code 200 + sentiment prédit = "positif" + bonne structure des score_5_stars
  - un avis vide => code 422
  - un avis trop long => code 422
  - 3 avis issus de sample_reviews.csv avec un sentiment prévu bien prédit => code 200 + sentiment prévu = sentiment prédit

```bash
docker compose exec api-nlp pytest -v
============================================ test session starts =============================================
platform linux -- Python 3.11.18, pytest-8.3.4, pluggy-1.7.0 -- /usr/local/bin/python3.11
cachedir: .pytest_cache
rootdir: /app
configfile: pytest.ini
testpaths: tests
plugins: asyncio-0.24.0, anyio-4.6.2.post1
asyncio: mode=Mode.STRICT, default_loop_scope=function
collected 7 items                                                                                            

tests/test_health.py::test_health_endpoint_returns_200 PASSED                                          [ 14%]
tests/test_predict.py::test_predict_avis_positif PASSED                                                [ 28%]
tests/test_predict.py::test_predict_texte_vide_trop_long[] PASSED                                      [ 42%]
tests/test_predict.py::test_predict_texte_vide_trop_long[Ce texte est vraiment beaucoup trop loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong !] PASSED [ 57%]
tests/test_predict.py::test_parametre_3_avis_coorects[H\xf4tel d'une m\xe9diocrit\xe9 rare. Bruit de plomberie toute la nuit, et personne pour s'en occuper.-n\xe9gatif] PASSED [ 71%]
tests/test_predict.py::test_parametre_3_avis_coorects[R\xe9ception agr\xe9able, chambre r\xe9cemment r\xe9nov\xe9e, beau bar \xe0 vins en bas. Tr\xe8s bonne adresse.-positif] PASSED [ 85%]
tests/test_predict.py::test_parametre_3_avis_coorects[S\xe9jour correct sans plus. La chambre fait son \xe2ge mais reste fonctionnelle pour une nuit.-neutre] PASSED [100%]

============================================= 7 passed in 5.07s ==============================================
```

| Variable (`.env`) | Défaut | Usage |
|---|---|---|
| `MODEL_NAME_HF` | `cmarkea/distilcamembert-base-sentiment` | Modèle HF à charger |
| `MAX_TEXT_LENGTH` | `2000` | Validation Pydantic (longueur max texte) |

---

