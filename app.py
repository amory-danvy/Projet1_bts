from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, CV
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_difficile_a_deviner' # Nécessaire pour la sécurité des sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Fichier de base de données local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login' # Redirige vers 'login' si on essaie d'accéder à une page protégée
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Recharge l'utilisateur depuis la BDD via son ID stocké dans la session."""
    return User.query.get(int(user_id))

# --- Création de la BDD au démarrage ---
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Vérifier si l'utilisateur existe déjà
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ce nom d\'utilisateur existe déjà.', 'danger')
            return redirect(url_for('register'))
        
        # Créer le nouvel utilisateur avec mot de passe hashé
        new_user = User(username=username, password_hash=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Compte créé ! Connectez-vous.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord : Liste des CVs de l'utilisateur."""
    user_cvs = CV.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', cvs=user_cvs)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_cv():
    """Création d'un nouveau CV."""
    if request.method == 'POST':
        title = request.form.get('title')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        experience = request.form.get('experience')
        education = request.form.get('education')
        theme = request.form.get('theme')
        
        new_cv = CV(
            title=title,
            fullname=fullname,
            email=email,
            phone=phone,
            address=address,
            experience=experience,
            education=education,
            theme=theme,
            author=current_user
        )
        
        db.session.add(new_cv)
        db.session.commit()
        
        flash('CV créé avec succès !', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('create_cv.html')

@app.route('/view/<int:id>')
def view_cv(id):
    """Affichage du CV final (Public ou Privé, ici accessible si on a le lien pour simplifier)."""
    cv = CV.query.get_or_404(id)
    return render_template('view_cv.html', cv=cv)

if __name__ == '__main__':
    app.run(debug=True)
