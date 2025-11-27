from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, CV
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_difficile_a_deviner'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads' # Dossier pour les images

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialisation des extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Création de la BDD au démarrage ---
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ce nom d\'utilisateur existe déjà.', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, password_hash=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Compte créé ! Connectez-vous.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_cvs = CV.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', cvs=user_cvs)

import json # Import nécessaire

# ... (reste du code)

@app.route('/create', methods=['GET', 'POST'])
@app.route('/edit/<int:cv_id>', methods=['GET', 'POST'])
@login_required
def create_cv(cv_id=None):
    cv = None
    if cv_id:
        cv = CV.query.get_or_404(cv_id)
        if cv.author != current_user:
            flash('Accès non autorisé.', 'danger')
            return redirect(url_for('dashboard'))
            
    if request.method == 'POST':
        title = request.form.get('title')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        theme = request.form.get('theme')
        color_theme = request.form.get('color_theme', 'Blue')
        
        # Récupération des listes pour Expérience
        exp_titles = request.form.getlist('experience_title[]')
        exp_dates = request.form.getlist('experience_date[]')
        exp_descs = request.form.getlist('experience_desc[]')
        
        # Construction de la liste de dictionnaires pour Expérience
        experience_list = []
        for i in range(len(exp_titles)):
            experience_list.append({
                'title': exp_titles[i],
                'date': exp_dates[i],
                'description': exp_descs[i]
            })
            
        # Récupération des listes pour Formation
        edu_titles = request.form.getlist('education_title[]')
        edu_dates = request.form.getlist('education_date[]')
        edu_descs = request.form.getlist('education_desc[]')
        
        # Construction de la liste de dictionnaires pour Formation
        education_list = []
        for i in range(len(edu_titles)):
            education_list.append({
                'title': edu_titles[i],
                'date': edu_dates[i],
                'description': edu_descs[i]
            })

        # Récupération des Centres d'intérêt
        interests_list = request.form.getlist('interests[]')
        
        # Gestion de l'image
        image_filename = cv.profile_image if cv else 'default.jpg'
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        if cv:
            # Mise à jour
            cv.title = title
            cv.fullname = fullname
            cv.email = email
            cv.phone = phone
            cv.address = address
            cv.experience = json.dumps(experience_list)
            cv.education = json.dumps(education_list)
            cv.interests = json.dumps(interests_list)
            cv.theme = theme
            cv.color_theme = color_theme
            cv.profile_image = image_filename
            flash('CV mis à jour avec succès !', 'success')
        else:
            # Création
            new_cv = CV(
                title=title,
                fullname=fullname,
                email=email,
                phone=phone,
                address=address,
                experience=json.dumps(experience_list),
                education=json.dumps(education_list),
                interests=json.dumps(interests_list),
                theme=theme,
                color_theme=color_theme,
                profile_image=image_filename,
                author=current_user
            )
            db.session.add(new_cv)
            flash('CV créé avec succès !', 'success')
            
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    # Préparation des données pour le template en cas d'édition
    if cv:
        try:
            cv.experience_data = json.loads(cv.experience) if cv.experience else []
            cv.education_data = json.loads(cv.education) if cv.education else []
            cv.interests_data = json.loads(cv.interests) if cv.interests else []
        except:
            cv.experience_data = []
            cv.education_data = []
            cv.interests_data = []
        
    return render_template('create_cv.html', cv=cv)

@app.route('/view/<int:id>')
def view_cv(id):
    cv = CV.query.get_or_404(id)
    
    # On décode le JSON pour l'envoyer au template sous forme d'objet Python utilisable
    try:
        cv.experience_data = json.loads(cv.experience) if cv.experience else []
        cv.education_data = json.loads(cv.education) if cv.education else []
        cv.interests_data = json.loads(cv.interests) if cv.interests else []
    except:
        cv.experience_data = []
        cv.education_data = []
        cv.interests_data = []
        
    return render_template('view_cv.html', cv=cv)



if __name__ == '__main__':
    app.run(debug=True)
