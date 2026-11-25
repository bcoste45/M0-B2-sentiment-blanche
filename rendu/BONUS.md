# M0-B2 — Bonus

## H — Mesurer l'effet d'un autre découpage 5★ → 3 classes

Les 30 avis de sample_reviews.csv sont récupérés, prédits et sauvegardés dans scores_30_avis.json sous la forme ' {id, attendu :(sentiment attendu), note_client, scores_5_stars : (score issu du predict)} '.  
On applique les règles suivantes de mapping pour déterminer le sentiment prédit d'après le score_5_stars.

| Règle | Étoile retenue | Négatif | Neutre | Positif |
|---|---|---|---|---|
| A | la plus probable | 1-2 | 3 | 4-5 |
| B | la plus probable | 1 | 2-3 | 4-5 |
| C | la plus probable | 1-2 | 3-4 | 5 |
| S | aucune : on **somme les probabilités** par groupe (1-2 / 3 / 4-5), le plus gros total l'emporte | | | |

L'on obtient comme résultats :
#### Règle A
    Nombre d'avis bien classé = 24/30
 
    Matrice de confusion : 
    |attendu\predit| négatif | neutre  | positif |
    |--------------|---------|---------|---------|
    |   négatif    |    8    |    2    |    1    |
    |   neutre     |    1    |    6    |    1    |
    |   positif    |    0    |    1    |    10   |
    
    Avis n°5 est un négatif manqué
    Avis n°18 est une fausse alerte.


#### Règle B
    Nombre d'avis bien classé = 21/30
    
    Matrice de confusion : 
    |attendu\predit| négatif | neutre  | positif |
    |--------------|---------|---------|---------|
    |   négatif    |    4    |    6    |    1    |
    |   neutre     |    0    |    7    |    1    |
    |   positif    |    0    |    1    |    10   |
    
    Avis n°1 est un négatif manqué
Pas de fausse alerte.

#### Règle C
    Nombre d'avis bien classé = 21/30
    
    Matrice de confusion : 
    |attendu\predit| négatif | neutre  | positif |
    |--------------|---------|---------|---------|
    |   négatif    |    8    |    3    |    0    |
    |   neutre     |    1    |    7    |    0    |
    |   positif    |    0    |    5    |    6    |
    
    Avis n°5 est un négatif manqué
    Avis n°18 est une fausse alerte.

#### Règle S
    Nombre d'avis bien classé = 25/30
    
    Matrice de confusion : 
    |attendu\predit| négatif | neutre  | positif |
    |--------------|---------|---------|---------|
    |   négatif    |    10   |    0    |    1    |
    |   neutre     |    2    |    5    |    1    |
    |   positif    |    0    |    1    |    10   |
    
    Avis n°12 est un négatif manqué
    Avis n°4 est une fausse alerte.


- La règle S est celle qui classe le plus d'avis correctment (25/30) mais également celle qui manque le moins de négatif, mais par contre c'est celle qui génère le plus de fausse alerte.

- J'avais choisi la règle S.

- On remarque que , dans sample_reviews.csv, pour une note_client de 1 ou 2, le sentiment est négatif; pour 3, il est neutre; et pour 4 ou 5, il est positif. Le sentiment attendu est surement fabriqué suivant unr règle similaire à S ou A.

- Le score obtenu ne peut être totalement fiable car il est issu que d'un seul échantillon de seulement 30 avis. Pour s'assurer de sa fiabilité, il faudrait que l'échantillon soit beaucoup plus fourni.

La règle que j'avais choisi est correcte vu qu'elle arrive à miniser les négatifs manqués.


## G — « Pourquoi pas un LLM généraliste ? »


## F — Endpoint `/predict/batch`
#### Mesure des durées des différents predict
On utilise le script rendu/mesure_predict_batch.py qu'on lance depuis la racine du repo, stack démarrée. 

```bash
python .\rendu\mesure_predict_batch.py
Temps pour 30 avis avec /predict = 2678.258000058122 ms
Temps pour 30 avis avec /predict/batch = 634.3099999940023 ms
Temps pour 30 avis avec /predict/batchV2 = 669.3268000381067 ms

python .\rendu\mesure_predict_batch.py
Temps pour 30 avis avec /predict = 1512.2090999502689 ms
Temps pour 30 avis avec /predict/batch = 523.2733000302687 ms
Temps pour 30 avis avec /predict/batchV2 = 553.4031999995932 ms

python .\rendu\mesure_predict_batch.py
Temps pour 30 avis avec /predict = 1653.3335000276566 ms
Temps pour 30 avis avec /predict/batch = 676.6191000351682 ms
Temps pour 30 avis avec /predict/batchV2 = 535.171499941498 ms
```

Médianes :
- /predict :  1653.3335000276566 ms
- /predict/batch : 634.3099999940023 ms
- /predict/batchV2 : 553.4031999995932 ms

Le /predict est plus long car il lance 30 appels à l'API, ainsi qu'à CamemBERT, ce qui met plus de temps.
Les deux autres ont un temps similaires.


## E — Healthcheck dimensionné sur la réalité