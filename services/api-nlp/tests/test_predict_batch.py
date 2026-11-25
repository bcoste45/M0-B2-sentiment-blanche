# un lot de 3 textes → 200, 3 résultats dans le bon ordre ; 
# liste vide → 422 ; 
# 33 textes → 422.

import pytest
from fastapi.testclient import TestClient

from app.main import app

#connexion client une seule fois
# Fixture client
@pytest.fixture(scope="module")
def fixture_client():
    with TestClient(app) as client: 
        yield client

def getResponseBatchV1(fixture_client, textes):
    return fixture_client.post(
            "/predict/batch", 
            json={"textes": textes}
        )

def getResponseBatchV2(fixture_client, textes):
    return fixture_client.post(
            "/predict/batchV2", 
            json={"textes": textes}
        )


def test_3textes_OK_V1(fixture_client):
    textes = ["super","nul","correct"]
    response = getResponseBatchV1(fixture_client,textes)    
    assert response.status_code == 200    
    j = response.json()    
    assert "liste_sentiments" in j
    listeSentiments = j["liste_sentiments"]
    assert listeSentiments[0]["sentiment"]=="positif"
    assert listeSentiments[1]["sentiment"]=="négatif"
    assert listeSentiments[2]["sentiment"]=="neutre"

def test_listetextes_vide_V1(fixture_client):
    textes = []
    response = getResponseBatchV1(fixture_client,textes)
    assert response.status_code == 422   

def test_trop_textes_V1(fixture_client):
    textes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33"]
    response = getResponseBatchV1(fixture_client,textes)
    assert response.status_code == 422   


def test_3textes_OK_V2(fixture_client):
    textes = ["super","nul","correct"]
    response = getResponseBatchV2(fixture_client,textes)    
    assert response.status_code == 200    
    j = response.json()    
    assert "liste_sentiments" in j
    listeSentiments = j["liste_sentiments"]
    assert listeSentiments[0]["sentiment"]=="positif"
    assert listeSentiments[1]["sentiment"]=="négatif"
    assert listeSentiments[2]["sentiment"]=="neutre"

def test_listetextes_vide_V2(fixture_client):
    textes = []
    response = getResponseBatchV2(fixture_client,textes)
    assert response.status_code == 422   

def test_trop_textes_V2(fixture_client):
    textes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33"]
    response = getResponseBatchV2(fixture_client,textes)
    assert response.status_code == 422   

