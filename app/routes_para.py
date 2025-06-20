
''''
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import app, db
from models import Admin

main = Blueprint('main', __name__)

@app.route('/')
def index():
    return "Aplicação Flask funcionando!"

@app.route(' /login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Create a route to add the first admin (you should protect or remove this in production)
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if Admin.query.first():
        return 'Admin already exists'
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin(email=email)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('setup.html') 


@main.route('/deshbord')
def home():
    return render_template('deshbord.html')


@main.route('/empresa')
def empresa():
    return render_template('empresa.html')

@main.route('/user')
def user():
    return render_template('user.html')

@main.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')

@main.route('/indicador')
def indicador():
    return render_template('indicador.html')

@main.route('/importardados')
def importardados():
    return render_template('importardados.html')
'''