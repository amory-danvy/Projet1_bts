from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialisation de l'extension SQLAlchemy (la base de données)
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Modèle pour les utilisateurs.
    Hérite de UserMixin pour faciliter la gestion avec Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Relation : Un utilisateur peut avoir plusieurs CVs
    cvs = db.relationship('CV', backref='author', lazy=True)

class CV(db.Model):
    """
    Modèle pour les CVs.
    Contient toutes les informations affichées sur le CV.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Titre du CV (ex: "Développeur Python")
    
    # Informations personnelles
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    
    # Contenu
    experience = db.Column(db.Text, nullable=True) # Texte libre pour simplifier
    education = db.Column(db.Text, nullable=True)  # Texte libre pour simplifier
    
    # Style
    theme = db.Column(db.String(50), default="Standard") # Pour choisir la couleur/style
    
    # Clé étrangère vers l'utilisateur
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
