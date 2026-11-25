
import csv
import json
import urllib.request
from pathlib import Path

API = "http://localhost:8000/predict"
SORTIE = Path(__file__).parent / "scores_30_avis.json"

resultats = []
with open("data/sample_reviews.csv", encoding="utf-8") as f:
    for ligne in csv.DictReader(f):
        requete = urllib.request.Request(
            API,
            data=json.dumps({"texte": ligne["texte"]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            corps = json.load(reponse)
        resultats.append({
            "id": int(ligne["id"]),
            "attendu": ligne["sentiment_attendu"],
            "note_client": int(ligne["note_client"]),
            "scores_5_stars": corps["scores_5_stars"],
        })

SORTIE.write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(resultats)} avis enregistrés dans {SORTIE}")