# Loguru — Mini-cours

> Brief associé : M0-B2 (tâche 5)
> Durée de lecture + pratique : ~30 min
> Pré-requis : la tâche 3 faite (`/predict` renvoie 3 classes). `loguru` est
> déjà installé dans l'image de l'API.

## Pourquoi cette techno ?

Tout service en production **doit** journaliser ce qu'il fait. Sinon :

- impossible de débugger une erreur signalée hier ;
- impossible de mesurer les performances ;
- impossible de prouver à un audit qui a fait quoi.

Le module `logging` de la stdlib Python existe pour ça, mais il a un défaut :
**il faut beaucoup de configuration boilerplate** pour des fonctions de base
(rotation, format, couleurs).

**Loguru** est l'alternative moderne, simple par défaut. Une seule ligne pour
logger, configuration prête à l'emploi pour les usages pro (rotation, retention,
compression).

**Alternatives à connaître :**

| Outil | Position |
|---|---|
| **`logging` (stdlib)** | Très flexible, mais verbeux. Standard quand on impose stdlib only. |
| **structlog** | Logs structurés (JSON), excellent pour pipeline ELK / Grafana Loki. Plus complexe. |
| **picologging** | Drop-in replacement performant de stdlib. Niche. |

Sur ce parcours, **Loguru est imposé** par les conventions techniques du projet. C'est notre standard.

## Concepts clés

- **Le `logger` global** : importé depuis `loguru`, partagé dans toute
  l'application. Pas besoin de l'instancier comme avec `logging.getLogger()`.
- **Niveaux standards** : `DEBUG` (verbeux), `INFO` (déroulé normal),
  `WARNING` (recoverable), `ERROR` (échec localisé), `CRITICAL` (service mort).
- **Sinks** : un sink = un endroit où vont les logs (console, fichier, fonction
  callback). On les ajoute via `logger.add(...)`.
- **Rotation** : redécoupe le fichier quand il atteint une taille (`"10 MB"`)
  ou un délai (`"1 day"`).
- **Retention** : durée de conservation des fichiers archivés (`"30 days"`).
- **Compression** : compresse automatiquement les fichiers archivés
  (`compression="zip"` ou `"gz"`).
- **`@logger.catch`** : décorateur qui logge automatiquement n'importe quelle
  exception remontée par la fonction décorée. Très pratique sur un endpoint API.

## Exemple minimal qui tourne

```python
# Versions testées : python 3.11+, loguru 0.7+
from loguru import logger

# 1. Sortie console : déjà active par défaut, formatée et colorée
logger.info("Démarrage du service")
logger.warning("Attention, cache vide")
logger.error("Échec de l'appel externe")

# 2. Ajouter un fichier de logs avec rotation, retention, compression
logger.add(
    "logs/api.log",
    rotation="10 MB",        # nouveau fichier dès que 10 Mo atteints
    retention="30 days",     # garde 30 jours d'historique
    compression="zip",       # compresse les fichiers archivés
    level="INFO",            # ne logge pas les DEBUG dans ce fichier
)

# 3. Logger une exception proprement
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Calcul impossible")  # logge avec stacktrace complet

# 4. Décorateur @logger.catch : capture toute exception non gérée
@logger.catch
def predire(data: dict) -> str:
    if not data:
        raise ValueError("data vide")
    return "ok"

predire({})   # ValueError logguée automatiquement, pas besoin de try/except
```

> L'exemple ci-dessus est **facultatif, hors conteneur** : il demande un
> environnement Python local avec `loguru`. Tu peux passer directement à
> l'exercice, qui se fait dans Docker.

Si tu le lances, tu vois :

- la console affiche les messages colorés ;
- un dossier `logs/` apparaît avec `api.log` ;
- au bout de 10 Mo (ou en testant manuellement), un fichier daté apparaît.

## Exercice guidé

Dans le squelette **M0-B2**, ajoute le logging Loguru à l'endpoint `/predict`
de `services/api-nlp/app/main.py` (branché sur `predict_sentiment()` à la
tâche 3).

**Cherche par toi-même** en t'appuyant sur les *Concepts clés* et l'*Exemple
minimal* (étapes 1-2 du script ci-dessus). La solution est masquée plus bas — à
révéler seulement après ta tentative.

**Tâches :**

1. Dans `app/main.py`, juste après la configuration `logger.add(sys.stderr, ...)`
   déjà présente, ajouter un **sink fichier** pointant vers `logs/api.log`
   avec rotation `"5 MB"`, retention `"7 days"`, compression `"zip"`, niveau
   `INFO`, et `enqueue=True` (safe pour contextes async / multi-thread).
   Penser à créer le dossier `logs/` via `pathlib`. Dans le conteneur,
   `logs/` est le dossier `/app/logs`, déjà monté sur `./logs` de ton repo.
2. Dans la route `/predict`, après la prédiction, écrire **une seule ligne**
   `INFO` qui contient : le texte reçu **tronqué à 80 caractères**
   (`payload.texte[:80]`), le **sentiment** prédit et la **latence en ms**
   (déjà calculée dans la réponse : `result.latence_ms`).
3. Vérifier que `logs/` est dans `.gitignore` (c'est déjà le cas dans le
   template).
4. Reconstruire (`docker compose up --build -d`), lancer 5 requêtes à
   `/predict` (Swagger ou curl), puis lire les logs de deux façons :
   `docker compose logs api-nlp` et le fichier `logs/api.log`.

✅ **Résultat attendu** :
- `docker compose logs api-nlp` montre une ligne par requête `/predict` ;
- fichier `logs/api.log` avec la même ligne INFO par requête ;
- le texte est coupé à 80 caractères, jamais l'avis complet ;
- le sentiment et la latence sont visibles sur la ligne.

<details>
<summary>🔒 <strong>Solution</strong> — clique pour révéler (après avoir cherché)</summary>

```python
# app/main.py, juste après `logger.add(sys.stderr, ...)`
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logger.add(
    LOG_DIR / "api.log",
    rotation="5 MB",
    retention="7 days",
    compression="zip",
    level="INFO",
    enqueue=True,            # safe pour les contextes async / multi-thread
)
```

```python
# dans la route /predict, à la place du `return inference.predict_sentiment(...)`
result = inference.predict_sentiment(state["pipeline"], payload.texte, MODEL_NAME)
logger.info(
    "predict | texte={!r} | sentiment={} | latence={} ms",
    payload.texte[:80],
    result.sentiment,
    result.latence_ms,
)
return result
```

Exemple de ligne obtenue :

```
2026-11-16 10:12:03.512 | INFO     | app.main:predict:140 - predict | texte='Personnel charmant, chambre impeccable, on reviendra !' | sentiment=positif | latence=95.3 ms
```

</details>

⭐ **Bonus** : utiliser un format JSON pour les logs fichier (utile en M5 si tu
ingères les logs dans Grafana Loki). Indice : Loguru accepte une fonction
de formatage personnalisée passée au paramètre `format=`. La fonction
reçoit un `record` (dict) et doit retourner une string.

<details><summary>▶ Voir une solution possible</summary>

```python
def json_formatter(record):
    import json
    return json.dumps({
        "ts": record["time"].isoformat(),
        "level": record["level"].name,
        "msg": record["message"],
        "module": record["name"],
    }) + "\n"

logger.add("logs/api.jsonl", format=json_formatter, rotation="5 MB")
```

</details>

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| Oublier `enqueue=True` en contexte async / multi-thread | Corruption / interleaving des logs sous charge. |
| Oublier `logs/` dans `.gitignore` | Fichiers de logs commités (potentiellement plusieurs Mo, parfois secrets). |
| Logger des **secrets / PII** dans les messages (tokens, mots de passe, données perso) | Fuite de données dans les logs archivés. |
| Utiliser un seul niveau global (pas de niveau par sink) | DEBUG flood le fichier de prod, ou INFO masque les `WARNING` critiques. |
| Appeler `logger.exception(...)` **hors** d'un `except` actif | Pas de stack trace capturé → devient un `logger.error` standard sans le contexte. |
| Rotation trop fréquente (`"1 KB"`) | Centaines de fichiers archivés, outils d'analyse cassés. |

**Symptôme → cause probable**

| Symptôme | Cause probable |
|---|---|
| Logs entrelacés / corrompus sous charge | `enqueue=True` oublié dans `logger.add(...)` |
| `logger.exception` n'affiche pas la stack trace | Appelé hors d'un bloc `except` actif |
| Fichier `api.log` commité par erreur | `logs/` pas dans `.gitignore` |
| Le fichier de prod ne contient que des DEBUG inutiles | Pas de `level="INFO"` sur le sink fichier |
| 200 fichiers `api.log.YYYY-MM-DD.zip` en 1 journée | Rotation trop agressive (passer à `"10 MB"` ou `"1 day"`) |

## Pour aller plus loin

- **Doc officielle Loguru** : <https://loguru.readthedocs.io/>
- **Référence legacy OPCO ATLAS** (partie « Loguru » : rotation, retention,
  compression, exemple complet d'API sur 1 page) : disponible **à la demande
  via Discord** auprès de la formatrice. Bon complément pour le détail de
  chaque option.
- **Comparaison Loguru vs logging stdlib** :
  <https://github.com/Delgan/loguru#features>

⭐ **Pour M5** (déploiement/monitoring), on enverra ces logs dans un
collector (Loki, Elasticsearch). Le format JSON cité plus haut sera précieux à
ce moment-là.

## Vérification (checklist apprenant)

- [ ] Mon endpoint `/predict` logge **une ligne INFO par requête** : texte tronqué à 80 caractères, sentiment, latence en ms.
- [ ] Je retrouve cette ligne avec `docker compose logs api-nlp` **et** dans `logs/api.log`.
- [ ] Le dossier `logs/` est créé automatiquement.
- [ ] `logs/` est dans mon `.gitignore`.
- [ ] La rotation est configurée (`rotation="5 MB"` dans le code ; la tester en générant 5 Mo de logs est facultatif, non évalué).
- [ ] Je sais expliquer en 1 minute la différence **DEBUG / INFO / WARNING / ERROR**.
- [ ] Je sais ce que fait `enqueue=True` (thread-safe, indispensable en API).