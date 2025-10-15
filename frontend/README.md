# JobLexa Analytics (Frontend-React.js)

**Le frontend de JobLexa Analytics est une application web monopage (SPA) construite avec React, visant à fournir une interface utilisateur moderne, rapide et réactive pour interagir avec le moteur d'analyse Python/FastAPI.**

## Stack Technique Frontend
- Framework: **React.js**
- Routage: **React Router DOM**
- Communication API: Axios 

## Fonctionnalités
1. Flux Utilisateur Sécurisé (Auth Flow)
Authentification : Gestion des connexions et inscriptions locales, ainsi que du flux de redirection Google OAuth.

Protection des Routes : Utilisation d'un composant ProtectedRoute pour garantir que le tableau de bord est inaccessible sans un jeton JWT valide stocké dans le navigateur.

2. Le Moteur de Correspondance (Core Functionality)
Formulaires Synchronisés : Les formulaires sont conçus pour s'assurer que l'utilisateur doit lancer la "Recherche de Compétences" (/jobmatch/skills) et que ces paramètres sont sauvegardés pour l'étape suivante.

Upload Asynchrone : Gère le téléchargement des fichiers CV (.pdf, .docx) à l'aide de FormData, avec un retour d'état de chargement clair pour l'utilisateur.

3. Affichage des Données (Visualisation)
Résultats de l'IA : Affiche clairement le Pourcentage de Correspondance (AI Match Score), les Compétences Manquantes (liste), et le Feedback Qualitatif (suggestion d'amélioration) renvoyé par l'API OpenAI.


## Apercu
![JobLexa Analytics Demo](https://drive.google.com/file/d/1X1dfcXIZArvEaELx8D0zq9OD6VVy8CDs/view?usp=drive_link)
