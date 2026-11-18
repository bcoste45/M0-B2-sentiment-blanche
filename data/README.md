# Dataset `sample_reviews.csv`

30 avis clients fictifs en français (Aubergine Hôtels), avec le sentiment
attendu en 3 classes.

## Usage

- Tâche 6 : choisir des avis dont le sentiment attendu est connu pour le test paramétré.
- Livrable B : passer les 30 avis dans ton API, comparer le sentiment attendu
  et le sentiment prédit, repérer les erreurs.

## Schéma du CSV

| Colonne | Type | Description |
|---|---|---|
| `id` | int | Identifiant 1-30 |
| `hotel` | str | Établissement fictif (préfixé *Aubergine*) |
| `texte` | str | Avis en français |
| `note_client` | int | Note 1-5 (contextuelle, **non utilisée** par le modèle) |
| `sentiment_attendu` | str | Sentiment attendu en 3 classes (`négatif`/`neutre`/`positif`) |

Encodage UTF-8, séparateur `,`, header présent.

## Garde-fous

- Aucun établissement réel : tous fictifs.
- Aucune donnée personnelle identifiable.
