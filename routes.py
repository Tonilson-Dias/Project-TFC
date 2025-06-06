from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import app, db
from models import Admin
from datetime import datetime, date
import re
import os
from werkzeug.utils import secure_filename


def validar_nome(nome):
    return re.match(r'^[A-Za-zÀ-ÿ\s]{3,100}$', nome)


def validar_telefone(telefone):
    return re.match(r'^\d{10,11}$', telefone)


def validar_senha(senha):
    # Pelo menos 8 caracteres, letras e números
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', senha)


def flash_redirect(message, category, endpoint):
    flash(message, category)
    return redirect(url_for(endpoint))


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        else:
            return flash_redirect('Email ou senha inválidos', 'danger', 'login')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    database_name = database_url.split('/')[-1].split('?')[0] if database_url else 'Desconhecido'
    admins = Admin.query.all()
    return render_template('dashboard.html', admin_bd=database_name, admins=admins)

''''
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if Admin.query.first():
        return 'Administrador já existe.'

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return flash_redirect('Email e senha são obrigatórios.', 'danger', 'setup')

        admin = Admin(email=email) # type:ignore
        admin.set_password(password)

        try:
            db.session.add(admin)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            return flash_redirect('Erro ao criar administrador. Tente novamente.', 'danger', 'setup')

    return render_template('setup.html')
    '''

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cargo = request.form.get('cargo', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([nome, email, cargo, password, confirm_password]):
            return flash_redirect('Todos os campos obrigatórios devem ser preenchidos', 'danger', 'register')

        if not validar_nome(nome):
            return flash_redirect('Nome inválido', 'danger', 'register')

        if telefone and not validar_telefone(telefone):
            return flash_redirect('Telefone inválido', 'danger', 'register')

        if password != confirm_password:
            return flash_redirect('As senhas não coincidem', 'danger', 'register')

        if not validar_senha(password):
            return flash_redirect('A senha deve ter no mínimo 8 caracteres, incluindo letras e números', 'danger', 'register')

        if Admin.query.filter_by(email=email).first():
            return flash_redirect('Email já cadastrado', 'danger', 'register')

        novo_usuario = Admin(
            nome=nome, # type:ignore
            email=email,# type:ignore
            telefone=telefone, # type:ignore
            cargo=cargo, # type:ignore
            data_cadastro=datetime.utcnow() # type:ignore
        )
        novo_usuario.set_password(password)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except Exception:
            db.session.rollback()
            return flash_redirect('Erro ao cadastrar usuário. Por favor, tente novamente.', 'danger', 'register')

    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/empresa')
@login_required
def empresa():
    return render_template('empresa.html')

@app.route('/indicador')
@login_required
def indicador():
    return render_template('indicador.html')


@app.route('/importardados')
@login_required
def relatorio():
    return render_template('relatorio.html')

@app.route('/importardados')
@login_required
def importardados():
    return render_template('importardados.html')

@app.route('/atualizar_perfil', methods=['POST'])
@login_required
def atualizar_perfil():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    telefone = request.form.get('telefone', '').strip()
    cargo = request.form.get('cargo', '').strip()
    nova_senha = request.form.get('nova_senha', '')

    if not all([nome, email, cargo]):
        return flash_redirect('Todos os campos obrigatórios devem ser preenchidos', 'danger', 'profile')

    if not validar_nome(nome):
        return flash_redirect('Nome inválido', 'danger', 'profile')

    if telefone and not validar_telefone(telefone):
        return flash_redirect('Telefone inválido', 'danger', 'profile')

    email_exists = Admin.query.filter(Admin.email == email, Admin.id != current_user.id).first()
    if email_exists:
        return flash_redirect('Email já está em uso por outro usuário', 'danger', 'profile')

    current_user.nome = nome
    current_user.email = email
    current_user.telefone = telefone
    current_user.cargo = cargo

    if nova_senha:
        if not validar_senha(nova_senha):
            return flash_redirect('A senha deve ter no mínimo 8 caracteres, incluindo letras e números', 'danger', 'profile')
        current_user.set_password(nova_senha)

    try:
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao atualizar perfil. Por favor, tente novamente.', 'danger')

    return redirect(url_for('profile'))


@app.route('/upload_foto', methods=['POST'])
@login_required
def upload_foto():
    foto = request.files.get('foto')
    if not foto or foto.filename == '':
        return flash_redirect('Nenhum arquivo selecionado', 'danger', 'profile')

    if not foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # type: ignore
        return flash_redirect('Formato de arquivo não permitido. Use PNG, JPG, JPEG ou GIF.', 'danger', 'profile')

    hoje = date.today()
    caminho_relativo = f'img/{hoje.day}/{hoje.month}/{hoje.year}'
    caminho_completo = os.path.join(app.static_folder, caminho_relativo) # type: ignore
    os.makedirs(caminho_completo, exist_ok=True)

    filename = secure_filename(foto.filename) # type: ignore
    nome_arquivo = f"{current_user.id}_{filename}"

    # Remove foto antiga
    if current_user.foto_perfil:
        try:
            caminho_antigo = os.path.join(app.static_folder, current_user.foto_perfil) # type: ignore
            if os.path.exists(caminho_antigo):
                os.remove(caminho_antigo)
        except Exception as e:
            app.logger.error(f"Erro ao remover foto antiga: {e}")

    caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)
    foto.save(caminho_arquivo)

    current_user.foto_perfil = f'{caminho_relativo}/{nome_arquivo}'

    try:
        db.session.commit()
        flash('Foto de perfil atualizada com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao atualizar foto de perfil. Por favor, tente novamente.', 'danger')

    return redirect(url_for('profile'))


@app.route('/excluir_conta', methods=['POST'])
@login_required
def excluir_conta():
    try:
        if current_user.foto_perfil:
            caminho_foto = os.path.join(app.static_folder, current_user.foto_perfil) # type: ignore
            if os.path.exists(caminho_foto):
                os.remove(caminho_foto)

        db.session.delete(current_user)
        db.session.commit()

        logout_user()
        flash('Sua conta foi excluída com sucesso.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao excluir conta: {e}")
        flash('Erro ao excluir conta. Por favor, tente novamente.', 'danger')
        return redirect(url_for('profile'))

@app.route('/atualizar_usuario/<int:user_id>', methods=['POST'])
@login_required
def atualizar_usuario(user_id):
    admin = Admin.query.get_or_404(user_id)
    
    # Verificar se o usuário tem permissão para editar
    if not current_user.is_authenticated:
        flash('Você não tem permissão para editar usuários.', 'danger')
        return redirect(url_for('user'))
    
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    telefone = request.form.get('telefone', '').strip()
    cargo = request.form.get('cargo', '').strip()
    nova_senha = request.form.get('nova_senha', '')
    ativo = request.form.get('ativo') == '1'
    
    if not all([nome, email, cargo]):
        flash('Todos os campos obrigatórios devem ser preenchidos', 'danger')
        return redirect(url_for('user'))
    
    # Verificar se o email já está em uso por outro usuário
    email_exists = Admin.query.filter(Admin.email == email, Admin.id != user_id).first()
    if email_exists:
        flash('Email já está em uso por outro usuário', 'danger')
        return redirect(url_for('user'))
    
    try:
        admin.nome = nome
        admin.email = email
        admin.telefone = telefone
        admin.cargo = cargo
        admin.ativo = ativo
        
        if nova_senha:
            admin.set_password(nova_senha)
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
    
    return redirect(url_for('user'))
