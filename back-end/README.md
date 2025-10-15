# JobLexa Analytics (Backend-Python)

**JobLexa Analytics est une plateforme qui utilise l'intelligence artificielle pour analyser en temps réel les exigences du marché de l'emploi dans le secteur TI et optimiser le CV de l'utilisateur.**

---

##  Fonctionnalités Clés
- Authentification sécurisée par **JWT** et **Google OAuth 2.0**.
- **Extraction de Compétences :** Recherche de **compétences clés** selon le poste, la ville et la province.
- **Analyse CV par IA :** Calcul d'un score de correspondance (AI Match Score) et fourniture de suggestions d'amélioration ciblées.


---

##  Stack Technique & Architecture
- **Framework Principal :** **FastAPI** (pour l'API REST asynchrone).
- **Serveur :** **Uvicorn** (Serveur ASGI haute performance).
- **IA / NLP :** **OpenAI** (pour l'analyse de CV et le score de match) et **SpaCy** (pour l'extraction et la pondération des compétences).
- **Base de Données :** **SQLAlchemy (asynchrone)** pour la persistance des données utilisateur.
- **Validation :** **Pydantic** pour la validation automatique des schémas de données (requêtes/réponses).
- **Collecte de Données :** **SerpAPI** (pour l'accès aux données d'offres d'emploi).
- **Authentification :** **OAuth 2.0** (Google login) et **Python-JOSE** (gestion des jetons JWT).