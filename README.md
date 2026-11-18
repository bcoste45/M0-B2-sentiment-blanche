# M0-B2 — Squelette repo (sentiment FR · stack `docker compose`)

> **Repo template GitHub.** Une seule personne par binôme clique sur
> **« Use this template »** → **Create a new repository** → nomme le repo
> `M0-B2-sentiment-<prenom1>-<prenom2>` sur son compte GitHub, puis invite
> l'autre (Settings → Collaborators). Ne faites pas de fork.
> Qui crée le repo : mettez-vous d'accord, à l'oral ou par écrit. À défaut,
> c'est la personne dont le prénom vient en premier dans l'ordre alphabétique.
> L'autre lui donne son identifiant GitHub, à l'oral ou par message.
> 🧍 Poste solo : `M0-B2-sentiment-<prenom>`, sans invitation.
> Repo public, ou privé avec la formatrice invitée en lecture (son
> identifiant GitHub est donné sur Simplonline).
>
> Dans ce README, `<prenom>` = ton prénom en minuscules, sans accent, et
> `<user>` = le compte GitHub de la personne qui a créé le repo.

**Tout s'exécute dans Docker : ce brief ne demande aucun environnement virtuel
Python sur ta machine.**

Brief **M0-B2 « Déployer une IA NLP packagée — sentiment FR chez Aubergine
Hôtels »**, 8 h en 3 temps : séance 1 (tâches 1 à 4 ; 3 h 45, dont 3 h 05 de
tâches, le reste couvre le point d'étape, la pull request et la pause),
travail individuel (livrables A à D), séance 2 (tâches 5 et 6).
L'énoncé complet est publié sur **Simplonline** : c'est lui qui fait foi pour
les livrables et les critères. Ce README est votre tableau de bord au quotidien.

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

## 🌿 Travailler à deux (ou seul·e) — règles Git

**Seul `main` est corrigé.** Un travail resté sur une branche n'existe pas
pour la correction.

```bash
# Au quotidien, sur TA branche
git switch <prenom>
git add <fichiers> && git commit -m "feat(api): map 5 stars to 3 classes"
git push -u origin <prenom>

# Intégrer dans main : ouvre une Pull Request sur GitHub
#   base = main  ←  compare = <prenom>   puis « Merge pull request »
# (en binôme, l'autre relit avant de merger ; 🧍 poste solo : tu merges ta propre PR)

# Récupérer ce que l'autre a mergé (🧍 poste solo : ces trois lignes servent
# seulement à mettre ta branche à jour avec `main`)
git switch main && git pull
git switch <prenom> && git merge main
git push
# Refais ces trois lignes avant d'ouvrir chaque Pull Request.
```

- Une PR vers `main` **au minimum à la fin de chaque séance** et avant le rendu.
- Tes livrables individuels vont dans **`rendu/<prenom>/`** : chacun a son
  dossier, donc pas de conflit.
- Le `README.md` de la racine est commun : **une seule personne le modifie**,
  l'autre lui envoie son texte. Qui : mettez-vous d'accord, à l'oral ou par
  écrit. À défaut, c'est la personne dont le prénom vient en premier dans
  l'ordre alphabétique. 🧍 Poste solo : tu le modifies seul·e.
- Ne commite jamais directement sur `main`.
- Messages de commit : `type(scope): description`.
- Si `git merge main` annonce un conflit : ouvre le fichier, garde ce qu'il
  faut entre `<<<<<<<` et `>>>>>>>`, supprime ces marqueurs, puis
  `git add <fichier> && git commit && git push`. Si tu bloques (ou si tu as
  commité sur `main` par erreur) : ne force rien, demande dans le fil Discord
  du brief.

---

## 🧠 Modèle utilisé

**`cmarkea/distilcamembert-base-sentiment`** — DistilCamemBERT FR, 68 M
paramètres, ~270 Mo.

⚠️ Le modèle sort **5 étoiles** (`'1 star'` … `'5 stars'`). Le métier
(Aubergine Hôtels) veut **3 classes** (`négatif/neutre/positif`).

→ Tu dois implémenter le **mapping 5★ → 3 classes** dans
`services/api-nlp/app/inference.py`. **C'est le geste cœur de ce brief**
(adaptation d'un service au format métier — C6 N2). Écris ta règle dans le
commentaire `# DECISION:` **avant** de coder. Il n'y a pas de bonne réponse :
ce qui compte, ce sont tes 2 arguments métier.

---

## 📁 Structure du repo

```
M0-B2-sentiment-<prenom1>-<prenom2>/
├── docker-compose.yml             ← 2 services + healthcheck api-nlp
├── .env.example
├── services/
│   ├── api-nlp/                   ← FastAPI + transformers
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py            ← routes (lifespan + /health + /info + /predict)
│   │   │   ├── schemas.py         ← Pydantic ReviewIn / SentimentOut
│   │   │   └── inference.py       ← TON CODE + mapping 5→3
│   │   └── tests/
│   │       └── test_health.py     ← 1 test pytest qui passe (tu ajoutes test_predict.py)
│   └── ui-streamlit/              ← UI utilisateur
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app.py                 ← UI à compléter (brancher l'appel HTTP)
├── data/
│   └── sample_reviews.csv         ← 30 reviews FR fictives (Aubergine Hôtels)
├── postman/
│   └── M0-B2_collection.json      ← point de départ de ta collection
├── rendu/
│   └── <prenom>/                  ← TES livrables individuels (à créer)
│       ├── ANALYSE.md             ← schéma Mermaid + reviews mal classées + mapping
│       └── postman_collection.json
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
└── README.md (ce fichier — à compléter : ajoutez en haut 5 à 10 lignes sur votre service et les 3 preuves ; gardez le reste)
```

---

## ✏️ Endpoints fournis

| Endpoint | Statut au clone | Ce que tu dois faire |
|---|---|---|
| `GET /health` | ✅ fonctionnel | rien |
| `GET /info` | ✅ fonctionnel | rien |
| `POST /predict` | ❌ 501 Not Implemented | implémenter (avec mapping 5→3) |

L'UI Streamlit est lancée mais affiche **« API non branchée »** tant que tu
n'as pas branché l'appel HTTP dans `services/ui-streamlit/app.py`.

---

## 🧭 Démarche attendue

### Séance 1 — en binôme (ou poste solo)

Après la tâche 2, la formatrice poste 3 questions dans le fil
Discord du brief. Y répondre est facultatif, à l'oral ou dans le fil, jusqu'à
la fin de la séance.

| # | Étape | Mini-cours | Durée |
|---|---|---|---|
| 1 | Créer le repo, démarrer la stack | (ce README) | 30 min |
| 2 | Lire le squelette + la fiche du modèle, **écrire `# DECISION:`** | — | 30 min |
| 3 | Implémenter `/predict` + **mapping 5★ → 3 classes** | [`02_HuggingFace_Transformers`](./ressources/02_HuggingFace_Transformers_essentiel.md) | 1 h 15 |
| 4 | Brancher l'UI Streamlit à l'API | [`03_Streamlit`](./ressources/03_Streamlit_essentiel.md) + [`04_API_Integration`](./ressources/04_API_Integration_essentiel.md) | 50 min |
| ✔ | PR vers `main` | — | — |

**Après chaque modification de code : `docker compose up --build` (sinon le conteneur exécute l'ancienne version).** Voir [`01_DockerCompose`](./ressources/01_DockerCompose_essentiel.md).

En binôme : l'un sur l'étape 3, l'autre sur l'étape 4, puis échange à
mi-séance. Mécanique d'échange en 3 lignes :

1. chacun pousse sa branche (`git push -u origin <prenom>`) et ouvre une pull request vers `main` ;
2. l'autre la fusionne ;
3. chacun fait `git switch main && git pull`, puis `git switch <prenom> && git merge main`.

Explication mutuelle : à l'oral ou par écrit (commentaire de pull request), au choix.
Étape 4 : tant que `/predict` répond 501, teste d'abord l'affichage du message
d'erreur ; le résultat nominal se teste après la fusion de l'étape 3. Pour
tester le message « API arrêtée » : `docker compose stop api-nlp`, recharge
l'interface, puis `docker compose start api-nlp`.
🧍 Poste solo : étape 3 puis étape 4, pas d'échange.

### Entre les deux séances — individuel, dans `rendu/<prenom>/`

| # | Livrable | Priorité | Durée |
|---|---|---|---|
| A | `ANALYSE.md` partie 1 : **schéma Mermaid** + comment lancer | 🔴 prioritaire | 1 h |
| B | `ANALYSE.md` partie 2 : **≥ 3 reviews mal classées** + explication | 🔴 prioritaire | 1 h |
| C | `postman_collection.json` (les 5 requêtes fournies + au moins 3 ajoutées, dont un texte trop long → 422 et un avis piégeux de ton choix) | 🟠 important | 45 min |
| D | `ANALYSE.md` partie 3 : justification du mapping (½ page) | 🟠 important | 15 min |

### Séance 2 — finitions

| # | Étape | Mini-cours | Durée |
|---|---|---|---|
| 5 | Logging Loguru (texte tronqué : `texte[:80]`) | [`05_Loguru`](./ressources/05_Loguru_essentiel.md) | 30 min |
| 6 | Tests pytest `/predict` (≥ 3) | [`06_Pytest_API`](./ressources/06_Pytest_API_essentiel.md) | 35 min |
| ✔ | 3 preuves dans le README + PR vers `main` + lien sur Simplonline | — | — |
| E/F/G | **Bonus** : healthcheck personnalisé avec plus de tentatives · `/predict/batch` · « pourquoi pas un LLM ? » | — | — |

**Après chaque modification de code : `docker compose up --build` (sinon le conteneur exécute l'ancienne version).** Voir [`01_DockerCompose`](./ressources/01_DockerCompose_essentiel.md).

Cf. [`./ressources/README.md`](./ressources/README.md) pour le détail.

---

## 🎯 Ce qui compte vraiment

1. **Une stack qui tourne** avec healthcheck `healthy`.
2. **Le mapping 5★ → 3 classes implémenté et justifié** (le geste C6 N2).
3. **L'UI Streamlit branchée à l'API** via le réseau docker interne :
   l'interface appelle l'API via `API_URL` (valeur `http://api-nlp:8000` dans
   `docker-compose.yml`), pas `localhost`.
4. **≥ 3 tests pytest qui passent** depuis le conteneur.
5. **Ton `rendu/<prenom>/ANALYSE.md`** : schéma Mermaid, reviews mal classées,
   justification du mapping.
6. **Tout est dans `main`.**

### Les 3 preuves à coller dans ce README (à la place d'une démo)

```bash
docker compose ps                                  # api-nlp (healthy)
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"texte":"Personnel charmant, on reviendra !"}'
docker compose exec api-nlp pytest -v              # tests PASSED
```

Sous Windows (PowerShell), cette commande ne passe pas telle quelle : envoie la
même requête depuis Swagger (`/docs`) ou Postman et colle la réponse.

---

## ✅ Tests & environnement

```bash
docker compose exec api-nlp pytest -v      # tests dans le conteneur API
# après avoir ajouté ou modifié un test : docker compose up --build -d
docker compose ps                          # api-nlp doit être (healthy)
```

| Variable (`.env`) | Défaut | Usage |
|---|---|---|
| `MODEL_NAME_HF` | `cmarkea/distilcamembert-base-sentiment` | Modèle HF à charger |
| `MAX_TEXT_LENGTH` | `2000` | Validation Pydantic (longueur max texte) |

---

## 🆘 Bloqué·e ?

| Symptôme | À tenter |
|---|---|
| `docker compose up` bloqué sur `pulling/building` | Premier démarrage : plusieurs minutes (build puis téléchargement du modèle), patiente |
| `/predict` renvoie toujours 501 | `inference.py` pas encore complété, **ou image non reconstruite** : relance `docker compose up --build` |
| `/predict` renvoie `"1 star"` au lieu de `"négatif"` | Mapping 5→3 pas implémenté |
| L'UI affiche « API non branchée » | Compléter `app.py` dans `services/ui-streamlit/` |
| `Connection refused` depuis l'UI | `API_URL` = `http://api-nlp:8000` (nom de service), pas `localhost` |
| `ModuleNotFoundError` | Rebuild : `docker compose build --no-cache api-nlp` |
| Service `unhealthy` après 2 min | Au premier démarrage, le statut peut passer par `unhealthy` pendant le téléchargement du modèle, puis revenir à `healthy` : attends. Si ça persiste : `docker compose logs api-nlp` (réseau / mémoire / chargement modèle) |
| Conteneur tué sans message | Mémoire Docker inférieure à 6 Go : augmente-la dans Docker Desktop (au moins 6 Go) |

Logs en temps réel : `docker compose logs -f api-nlp`.

**Demande de l'aide**, à l'oral ou par écrit dans le fil Discord du brief :
les deux se valent. Par écrit, colle la commande lancée et le message
d'erreur complet. N'attends pas 30 min sur le même problème.
