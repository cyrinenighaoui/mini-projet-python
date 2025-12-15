# 🔎 Projet  – Moteur de recherche & exploration de corpus

**Réalisé par :** Cyrine Nighaoui  

Ce projet présente la **conception et l’implémentation d’un moteur de recherche textuel** basé sur des techniques de **Traitement Automatique du Langage Naturel **, appliquées à un corpus de discours politiques .
En complément des notebooks demandés, une **interface web entièrement dockerisée** a été développée afin de proposer une utilisation plus concrète et intuitive du moteur.

---

## 🚀 Présentation générale du projet

Le projet s’articule autour de :

- **Trois notebooks Jupyter**, couvrant l’ensemble du pipeline NLP
- Une **interface web interactive** via une API Flask
- Un **déploiement Docker**, ne nécessitant aucune installation locale (hors Docker Desktop)

---

## ⚙️ Dépendances et installations nécessaires

### Exécution via les notebooks ou en local (sans Docker)

Un environnement **Python 3.9+** est requis, ainsi que les bibliothèques suivantes :

```bash
pip install pandas numpy scikit-learn matplotlib ipywidgets flask
```
---

## 📓 Organisation des notebooks

### 🔹 Notebook 1 – Construction du corpus & pipeline NLP  
**`01_corpus_construction_and_nlp_pipeline.ipynb`**

Ce notebook constitue le **socle pédagogique du projet** et regroupe les notions abordées dans les **TD1 à TD7** :

- construction du corpus à partir de différentes sources,
- structuration des documents (auteurs, dates, sources),
- prétraitement et nettoyage des textes,
- analyse statistique (vocabulaire, TF, DF),
- premières fonctionnalités de recherche et de concordance.

👉 **Ce notebook peut être exécuté cellule par cellule** afin de suivre l’ensemble du raisonnement.

---

### 🔹 Notebook 2 – Construction du moteur de recherche TF-IDF  
**`02_search_engine_tfidf.ipynb`**

Ce notebook est dédié à la **création du moteur de recherche** :

- vectorisation du corpus,
- construction de la matrice Documents × Termes,
- entraînement du moteur TF-IDF,
- sauvegarde du moteur au format `engine.pkl`.

⚠️ **Remarque importante**  
Ce notebook a principalement servi à **entraîner et sauvegarder le moteur**.  
Il **n’est pas nécessaire de l’exécuter**, le moteur étant déjà fourni sous forme de fichier pickle et réutilisé dans le notebook suivant.

---

### 🔹 Notebook 3 – Interface de recherche & analyse temporelle  
**`03_interactive_search_interface_and_temporal_analysis.ipynb`**

Ce notebook correspond à la **partie fonctionnelle et démonstrative** du projet.

Il permet :
- l’utilisation directe du **moteur TF-IDF pré-entraîné**,
- des recherches interactives avec filtres (auteur, date),
- une exploration claire des résultats,
- une **analyse temporelle** de l’évolution d’un mot dans les discours.

👉 **Notebook qui permet de  tester concrètement le moteur de recherche**, sans recalcul coûteux.

---

## 🌐 Bonus – Interface web (Flask + Docker)

En complément des notebooks, une **interface web** a été développée afin d’améliorer l’expérience utilisateur et de proposer un cas d’usage plus réaliste.

### Fonctionnalités
- API REST développée avec **Flask**
- Intégration du moteur de recherche TF-IDF
- Interface simple et intuitive
- Aucune installation Python requise pour l’utilisateur

---

##  Lancer l’application web avec Docker

### Prérequis
- Docker Desktop **installé**
- Docker Desktop **lancé et en cours d’exécution**

---


###  Lancer l’application web avec Docker

Avant de lancer l’application, se placer dans le **dossier principal du projet** (`projet_python_cours`).  
Docker Desktop doit être **installé et en cours d’exécution**.

```bash
cd projet_python_cours
docker run -p 5000:5000 corpus-app

```

### 🛠️ Alternative – Exécution locale sans Docker

Si Docker ne fonctionne pas sur l’ordinateur, il est possible d’exécuter l’interface web **directement en local**.

Dans ce cas, se placer sur le commit **interface web**, puis s’assurer d’avoir un environnement Python fonctionnel ainsi que les dépendances nécessaires (Flask, HTML, CSS, JavaScript).  

Ensuite, se positionner dans projet_python_cours_api/api :

```bash
cd projet_python_cours/api
python app.py

