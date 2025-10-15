# JobLexa Analytics: L'Optimisation de carriere par l'IA
JobLexa Analytics est une plateforme Full Stack qui utilise l'IA pour analyser en temps réel 
les exigences du marché de l'emploi (hard et soft skills) et fournir à l'utilisateur un score de correspondance précis pour optimiser son CV.

## Fonctionnalités
L'application est est conçue autour de deux étapes principales à forte valeur ajoutée :
1.Extraction de Compétences : Identifie et pondère le Top 30 des compétences les plus demandées pour un poste et une région donnés, 
  en analysant les offres d'emploi en temps réel.
2.Analyse de CV par IA : Calcule un Score de Correspondance (AI Match Score) entre le CV de l'utilisateur et les exigences du marché, 
  et fournit des suggestions d'amélioration ciblées (compétences manquantes, conseils de rédaction).
3.Sécurité et Conformité : Authentification moderne par JWT et Google OAuth 2.0.

## Stack technique Globale
**Backend / API	FastAPI (Python)**	Framework asynchrone, rapide et performant, idéal pour les charges de travail I/O (appels API externes).
**Frontend / UI	React.js**	Application monopage (SPA) pour une interface utilisateur moderne et réactive.
**IA / NLP	OpenAI  & SpaCy**	Moteur d'analyse sémantique du CV et extraction/pondération des compétences (NLP avancé).
**Base de Données	SQLAlchemy (Async)**	ORM moderne pour la persistance des données utilisateur et des sessions de manière non bloquante.
**Collecte de Données	SerpAPI**	Accès structuré et fiable aux données d'offres d'emploi (Google Jobs).
**Sécurité	JWT / Passlib / OAuthlib**	Gestion de l'authentification sans état (stateless) et des tokens d'accès.
**Validation	Pydantic**	Validation automatique des données entrantes et sortantes (Data Validation).


## Apercu
![JobLexa Demo](https://drive.google.com/file/d/1X1dfcXIZArvEaELx8D0zq9OD6VVy8CDs/view?usp=sharing)

