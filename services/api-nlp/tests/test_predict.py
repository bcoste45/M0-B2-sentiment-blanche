
import pytest
from fastapi.testclient import TestClient

from app.main import app

# Fixture client
@pytest.fixture(scope="module")
def fixture_client():
    with TestClient(app) as client: 
        yield client

def getResponse(fixture_client, texte):
    return fixture_client.post(
            "/predict", 
            json={"texte":texte}
        )

def test_predict_avis_positif(fixture_client) -> None:
    """POST /predict avec un texte positif retourne 200 et une structure valide (avec sentiment=positif et scores_5_stars)."""
    response = getResponse(fixture_client, "Personnel charmant, chambre impeccable !")
    # Assert status code 200 (OK)
    assert response.status_code == 200
    j = response.json()
    assert j['sentiment'] == "positif"
    assert "scores_5_stars" in j
    assert "1 star" in j['scores_5_stars']
    assert "2 stars" in j['scores_5_stars']
    assert "3 stars" in j['scores_5_stars']
    assert "4 stars" in j['scores_5_stars']
    assert "5 stars" in j['scores_5_stars']

@pytest.mark.parametrize("texte_test", ["","Ce texte est vraiment beaucoup trop loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong !"])
def test_predict_texte_vide_trop_long(fixture_client,texte_test) -> None:
    """Test POST /predict cas non valides (texte vide ou trop long) => code 422"""
    response = getResponse(fixture_client, texte_test)
    # Assert status code 422 
    assert response.status_code == 422

@pytest.mark.parametrize("texte_test, sentiment_prevu", [
    ("Hôtel d'une médiocrité rare. Bruit de plomberie toute la nuit, et personne pour s'en occuper.","négatif"),
    ("Réception agréable, chambre récemment rénovée, beau bar à vins en bas. Très bonne adresse.","positif"),
    ("Séjour correct sans plus. La chambre fait son âge mais reste fonctionnelle pour une nuit.","neutre")
    ])
def test_parametre_3_avis_coorects(fixture_client, texte_test,sentiment_prevu) -> None:
    """Test POST /predict 3 cas valides (3 avis issu de sample_reviews) => code 200 + sentiment_prevu OK"""
    response = getResponse(fixture_client, texte_test)
    # Assert status code 200 (OK)
    assert response.status_code == 200    
    j = response.json()
    assert j['sentiment'] == sentiment_prevu



# Lancement : docker compose exec api-nlp pytest -v.