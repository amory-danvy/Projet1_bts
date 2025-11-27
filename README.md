# Générateur de CV

Un outil simple et efficace pour créer et gérer des CVs, développé en Python avec Flask.

## 🚀 Fonctionnalités

*   **Authentification** : Inscription et connexion sécurisées.
*   **Tableau de bord** : Gestion de vos différents CVs.
*   **Création facile** : Formulaire unique pour toutes les informations.
*   **Thèmes** : Choix entre plusieurs styles (Standard, Blue, Dark).
*   **Export PDF** : Impression propre directement depuis le navigateur.

## 🛠️ Installation

1.  **Cloner ou télécharger le projet.**
2.  **Installer uv (si nécessaire) :**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
3.  **Créer l'environnement et installer les dépendances :**
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

## ▶️ Utilisation

1.  **Lancer l'application :**
    ```bash
    # Si l'environnement est activé :
    python app.py
    # OU directement avec uv :
    uv run app.py
    ```
2.  **Ouvrir le navigateur :**
    Rendez-vous sur [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📂 Structure du projet

*   `app.py` : Code principal (Serveur).
*   `models.py` : Base de données.
*   `templates/` : Pages HTML.
*   `static/` : Styles CSS.
*   `EXPLICATION.md` : Documentation détaillée du code.

## 📝 Auteur

Projet réalisé pour présentation BTS.
