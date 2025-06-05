from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import app, db
from models import Admin
from datetime import datetime
import re
from sqlalchemy import inspect

@app.route('/', methods=['GET', 'POST'])
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
    # Get database name from configuration
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    database_name = database_url.split('/')[-1].split('?')[0]
    admins = Admin.query.all()
    return render_template('dashboard.html', admin_bd=database_name, admins=admins)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if Admin.query.first():
        return 'Admin already exists'
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin(email=email)  # type:ignore
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('setup.html')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        cargo = request.form.get('cargo')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validações
        if not all([nome, email, cargo, password, confirm_password]):
            flash('Todos os campos obrigatórios devem ser preenchidos', 'danger')
            return redirect(url_for('register'))

        if not re.match(r'^[A-Za-zÀ-ÿ\s]{3,100}$', nome):
            flash('Nome inválido', 'danger')
            return redirect(url_for('register'))

        if telefone and not re.match(r'^\d{10,11}$', telefone):
            flash('Telefone inválido', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('As senhas não coincidem', 'danger')
            return redirect(url_for('register'))

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            flash('A senha deve ter no mínimo 8 caracteres, incluindo letras e números', 'danger')
            return redirect(url_for('register'))

        # Verifica se já existe usuário com mesmo email
        if Admin.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'danger')
            return redirect(url_for('register'))

        # Cria novo usuário
        novo_usuario = Admin(
            nome=nome,
            email=email,
            telefone=telefone,
            cargo=cargo,
            data_cadastro=datetime.utcnow()
        )
        novo_usuario.set_password(password)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar usuário. Por favor, tente novamente.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html') 