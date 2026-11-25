
import csv
import time
import json
import urllib.request

API = "http://localhost:8000/predict"

avis : list[str] = []

#Mesure du temps mis par /predict, /predict/batch et /predict/batchV2 pour les 30 avis de sample_reviews.csv
def main():
    getAvisFromCsv()

    mesure_30Appels_predict()
    mesure_30Appels_predict_batchV1()
    mesure_30Appels_predict_batchV2()
    

def getAvisFromCsv():
    with open("data/sample_reviews.csv", encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            avis.append(ligne["texte"])

def mesure_30Appels_predict():
    t0 = time.perf_counter()
    for texte in avis:
        requete = urllib.request.Request(
            API,
            data=json.dumps({"texte": texte}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )        
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            corps = json.load(reponse)
    tps_inf = (time.perf_counter() - t0)*1000 #en ms
    print(f"Temps pour 30 avis avec /predict = {tps_inf} ms")

def mesure_30Appels_predict_batchV1():
    t0 = time.perf_counter()
    requete = urllib.request.Request(
        API+"/batch",
        data=json.dumps({"textes": avis}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )        
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        corps = json.load(reponse)    
    tps_inf = (time.perf_counter() - t0)*1000 #en ms
    print(f"Temps pour 30 avis avec /predict/batch = {tps_inf} ms")

def mesure_30Appels_predict_batchV2():
    t0 = time.perf_counter()
    requete = urllib.request.Request(
        API+"/batchV2",
        data=json.dumps({"textes": avis}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )        
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        corps = json.load(reponse)    
    tps_inf = (time.perf_counter() - t0)*1000 #en ms
    print(f"Temps pour 30 avis avec /predict/batchV2 = {tps_inf} ms")

main()