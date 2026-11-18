# Pytest pour API — Mini-cours

> Brief associé : M0-B2 (tâche 6)
> Pré-requis : la tâche 3 faite (`/predict` renvoie 3 classes). `pytest` et
> `httpx` sont déjà installés dans l'image de l'API ; les tests se lancent
> dans le conteneur.

## Pourquoi cette techno ?

Tester une API n'est **pas optionnel** quand on déploie un service en prod :

- chaque modification de code peut casser un endpoint ;
- chaque mise à jour de dépendance (FastAPI, scikit-learn, NumPy) peut casser
  la sérialisation ;
- chaque changement de modèle peut produire des prédictions incohérentes.

**pytest** est l'outil standard de test en Python. Combiné au **`TestClient`**
de FastAPI (basé sur httpx), il permet de tester une API **sans démarrer le
serveur** : on simule des requêtes en mémoire.

**Alternatives à connaître :**

| Outil | Position |
|---|---|
| **`unittest`** (stdlib) | OO, verbeux. Encore présent dans le legacy. |
| **`hypothesis`** | Property-based testing. Excellent en complément de pytest. |
| **`tavern`** | YAML-based tests d'API. Pour QA non-dev. |

Sur ce parcours, **pytest est imposé** par les conventions techniques du projet. On l'utilisera de M0 à M9.

## Concepts clés

- **Convention de nommage** : fichiers `test_*.py`, fonctions `test_*`. pytest
  les découvre automatiquement.
- **`assert`** : tu écris des assertions Python normales. Pas de `assertEqual`
  comme `unittest`. Si l'assert échoue, pytest affiche un diff lisible.
- **Fixture** : fonction qui prépare des données / objets avant un test, marquée
  `@pytest.fixture`. Très utile pour partager une `TestClient` entre tests.
- **`@pytest.mark.parametrize`** : exécute un même test avec plusieurs jeux de
  données. Évite la copie-colle.
- **`TestClient` (FastAPI)** : encapsule l'app, simule des requêtes HTTP via
  httpx. **Le `with TestClient(app) as client:` déclenche le lifespan**
  (chargement du modèle, etc.).
- **Codes HTTP attendus** : 200 (OK), 201 (créé), 400 (mauvaise requête métier),
  422 (validation Pydantic échouée), 500 (erreur serveur). À tester
  systématiquement.

## Exemple minimal qui tourne

```python
# Exemple facultatif, hors conteneur (demande un environnement Python local)
# tests/test_addition.py — exemple sans API pour comprendre pytest
def addition(a: int, b: int) -> int:
    return a + b


def test_addition_simple():
    assert addition(2, 3) == 5


def test_addition_negatifs():
    assert addition(-1, -2) == -3


import pytest

@pytest.mark.parametrize("a,b,attendu", [
    (0, 0, 0),
    (10, -3, 7),
    (1, 1, 2),
])
def test_addition_param(a, b, attendu):
    assert addition(a, b) == attendu
```

Lance (hors conteneur, facultatif) :

```bash
pytest -v
```

Tu vois `5 passed` (1 + 1 + 3 paramétrés). Si un cas échoue, pytest te montre
**la valeur attendue vs la valeur reçue** — gros gain de productivité par
rapport à `assertEqual`.

### Avec FastAPI TestClient

```python
# services/api-nlp/tests/test_health.py (livré au clone)
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_200() -> None:
    with TestClient(app) as client:    # ← le `with` déclenche le lifespan
        response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "model_loaded" in body
    assert body["status"] in {"ok", "loading", "error"}
    assert isinstance(body["model_loaded"], bool)
```

Le `with` est **important** : sans lui, le `lifespan` qui charge le modèle ne
s'exécute pas, et `model_loaded` serait `False`.

## Exercice guidé

Tu as déjà **1 test** pour `/health` dans `services/api-nlp/tests/test_health.py`
(livré au clone). **Ajoute 3 tests pour `/predict`** (dont un paramétré sur
3 avis) dans un nouveau fichier `services/api-nlp/tests/test_predict.py`.

**Cherche par toi-même** en t'appuyant sur la section *Concepts clés* et l'exemple
*Avec FastAPI TestClient* ci-dessus. La solution est masquée plus bas — à révéler
seulement après ta tentative.

**À écrire :**

1. Une **fixture `client`** de scope `module` qui ouvre un `TestClient(app)` avec
   `with` (pour déclencher le `lifespan`).
2. **Test cas nominal** : POST `/predict` avec `{"texte": "Personnel charmant,
   chambre impeccable, on reviendra !"}`, attendu `200` + `body["sentiment"]`
   parmi `négatif / neutre / positif` + les 5 clés de `scores_5_stars`.
3. **Test cas invalide** : POST avec `{"texte": ""}`, attendu `422` (validation
   Pydantic).
4. **Test paramétré** : `@pytest.mark.parametrize` sur **3 avis** que tu
   recopies dans ton test, avec le sentiment que ton mapping doit renvoyer.
   Recopie dans ton test le texte de 3 avis du CSV que ton mapping classe
   correctement (le fichier CSV n'est pas accessible depuis le conteneur :
   `data/` n'y est ni copié ni monté).

✅ **Résultat attendu** :
- `docker compose exec api-nlp pytest -v` affiche **6 tests** (1 sur `/health`
  + 1 nominal + 1 en 422 + 3 cas du test paramétré), tous PASSED.

> Les tests sont copiés dans l'image au build. **Après avoir ajouté ou modifié
> un test : `docker compose up --build -d`**, puis relance la commande
> `docker compose exec api-nlp pytest -v`.

<details>
<summary>🔒 <strong>Solution</strong> — clique pour révéler (après avoir cherché)</summary>

```python
# services/api-nlp/tests/test_predict.py
import pytest
from fastapi.testclient import TestClient

from app.main import app

SENTIMENTS = {"négatif", "neutre", "positif"}


@pytest.fixture(scope="module")
def client():
    """Fixture partagée : un seul TestClient pour tout le module."""
    with TestClient(app) as c:
        yield c


# 1. Cas nominal -> 200 + structure attendue
def test_predict_avis_positif_200(client):
    r = client.post(
        "/predict",
        json={"texte": "Personnel charmant, chambre impeccable, on reviendra !"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["sentiment"] in SENTIMENTS
    assert set(body["scores_5_stars"]) == {
        "1 star", "2 stars", "3 stars", "4 stars", "5 stars",
    }


# 2. Texte vide -> 422 (validation Pydantic)
def test_predict_texte_vide_422(client):
    r = client.post("/predict", json={"texte": ""})
    assert r.status_code == 422


# 3. Trois avis recopiés du CSV, avec le sentiment que le mapping A renvoie
@pytest.mark.parametrize(
    "texte,attendu",
    [
        ("Accueil glacial à la réception, chambre froide et bruyante, "
         "nous ne reviendrons pas.", "négatif"),
        ("Personnel charmant, chambre impeccable, petit-déjeuner copieux. "
         "On reviendra avec plaisir.", "positif"),
        ("Séjour correct sans plus. La chambre fait son âge mais reste "
         "fonctionnelle pour une nuit.", "neutre"),
    ],
)
def test_predict_avis_du_csv(client, texte, attendu):
    r = client.post("/predict", json={"texte": texte})
    assert r.status_code == 200
    assert r.json()["sentiment"] == attendu
```

Le test `test_predict_avis_du_csv` suppose le mapping A (1-2 → négatif, 3 →
neutre, 4-5 → positif) : les avis 1, 2 et 3 du CSV. Avec ton propre
mapping, choisis 3 avis que **ton** mapping classe correctement (vérifie-le
d'abord dans Swagger : certains avis du CSV sont mal classés, c'est l'objet
du livrable B).

</details>

⭐ **Bonus 1** : ajoute un test qui vérifie que la **somme des probabilités est
exactement 1.0** à `1e-9` près (montre que tu comprends `predict_proba`).

⭐ **Bonus 2** : ajoute un test « champ obligatoire manquant » → 422.

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| Oublier `with TestClient(app) as client:` | Le `lifespan` ne tourne pas → le modèle n'est pas chargé, `model_loaded:false`. |
| Définir une "fixture" sans `@pytest.fixture` | Ce n'est pas une fixture, c'est un appel direct → comportement imprévisible. |
| Mal comprendre `scope="module"` / `scope="session"` | State partagé entre tests, comportement dépendant de l'ordre. |
| Tests qui dépendent de l'**ordre** d'exécution | Faux verts en local, rouges en CI (anti-pattern majeur). |
| Tests qui font de **vrais appels réseau / fichier** | Lenteur + flakiness. Préférer `TestClient` ou mocker. |
| Assertions trop vagues : `assert r.status_code == 200` uniquement | Le test passe même si la réponse est incomplète/incorrecte. Vérifier aussi **structure**, **contenu** et **contrat métier**. |

**Symptôme → cause probable**

| Symptôme | Cause probable |
|---|---|
| `model_loaded:false` dans le test `/health` | `TestClient` utilisé sans `with` → lifespan pas exécuté |
| Tests qui passent seuls mais échouent en suite | State partagé entre tests (fixture mal scopée) ou ordre implicite |
| Un test devient lent / flaky en CI | Vrais appels réseau ou I/O — à mocker ou utiliser `TestClient` |
| `pytest` ne trouve aucun test | Fichier ou fonction sans préfixe `test_`, ou pas dans un répertoire reconnu |
| Assertion `assert r.json() == {...}` trop fragile | Inclure trop de détails dans le dict attendu — préférer assertions ciblées sur les clés contractuelles |

## Pour aller plus loin

- **Doc officielle pytest** : <https://docs.pytest.org/>
- **Doc TestClient FastAPI** : <https://fastapi.tiangolo.com/tutorial/testing/>
- **Référence legacy OPCO ATLAS** (partie « Pytest » : fixtures avec base
  SQLite, parametrize) : disponible **à la demande via Discord** auprès de la
  formatrice. Bon complément si tu veux des exemples plus poussés.
- **Coverage** : `pytest --cov=app` (nécessite `pytest-cov`). Vérifie que tu
  testes bien tout ton code.

⭐ **Pour M5** (CI/CD), tes tests pytest tourneront automatiquement sur chaque
push GitHub. Donc : **chaque test que tu écris aujourd'hui te protège pour
toujours.**

## Vérification (checklist apprenant)

- [ ] J'ai un fichier `services/api-nlp/tests/test_predict.py` avec **3 tests minimum**.
- [ ] `docker compose exec api-nlp pytest -v` affiche tous les tests PASSED (6 avec la solution du mini-cours).
- [ ] J'ai utilisé une **fixture** pour partager le `TestClient`.
- [ ] J'ai utilisé `@pytest.mark.parametrize` au moins une fois.
- [ ] Je sais expliquer pourquoi le `with TestClient(app) as ...:` est nécessaire.
- [ ] Je sais ce que veut dire **HTTP 422** et qui le déclenche (Pydantic).
- [ ] Je sais comment lancer un seul test ciblé : `docker compose exec api-nlp pytest tests/test_predict.py::test_predict_texte_vide_422 -v`.
- [ ] Je sais qu'après avoir ajouté ou modifié un test, il faut `docker compose up --build -d`.
