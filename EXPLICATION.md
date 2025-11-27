# Documentation du Projet Générateur de CV

Ce document explique le rôle de chaque fichier du projet pour faciliter la compréhension et la présentation.

## Fichiers Principaux

*   **`app.py`** : C'est le **cerveau** de l'application. Il configure Flask, gère la connexion à la base de données, définit toutes les routes (les URLs comme `/login`, `/dashboard`) et contient la logique métier (quoi faire quand on clique sur un bouton).
*   **`models.py`** : C'est le **plan de la base de données**. Il définit ce qu'est un "Utilisateur" (nom, mot de passe) et ce qu'est un "CV" (titre, expérience, etc.) pour que l'ordinateur sache comment stocker ces infos.
*   **`database.db`** : (Généré automatiquement) C'est le **fichier de stockage**. C'est là que sont réellement enregistrés les utilisateurs et leurs CVs. C'est comme un fichier Excel, mais géré par le code.

## Dossier `templates/` (Le Frontend / HTML)

C'est ici que se trouvent les pages que l'utilisateur voit. Elles utilisent **Jinja2** (le moteur de template de Flask) pour insérer des données dynamiques (comme le nom de l'utilisateur) dans le HTML.

*   **`base.html`** : Le **squelette** commun à toutes les pages. Il contient l'entête (HTML, chargement de Bootstrap) et la barre de navigation. Toutes les autres pages s'insèrent à l'intérieur de celle-ci pour éviter de répéter le code.
*   **`index.html`** : La **page d'accueil** publique. Elle présente le projet et invite à s'inscrire ou se connecter.
*   **`login.html`** : Le formulaire de **connexion**.
*   **`register.html`** : Le formulaire d'**inscription**.
*   **`dashboard.html`** : Le **tableau de bord** privé. Une fois connecté, l'utilisateur y voit la liste de ses CVs et peut en créer un nouveau.
*   **`create_cv.html`** : Le **formulaire de création** de CV. C'est là qu'on saisit ses expériences, études, et qu'on choisit le thème.
*   **`view_cv.html`** : La page de **visualisation finale** du CV. Elle est conçue pour être belle à l'écran et parfaite lors de l'impression (PDF).

## Dossier `static/`

*   **`style.css`** : Les **règles de style personnalisées**. Bien qu'on utilise Bootstrap pour le gros du travail, ce fichier sert à peaufiner les détails (couleurs des thèmes, mise en page spécifique pour l'impression).

## Résumé de la Stack Technique

*   **Python + Flask** : Pour la logique serveur (simple et robuste).
*   **SQLite** : Pour les données (léger, pas d'installation).
*   **Bootstrap 5** : Pour un design propre et réactif sans effort.
