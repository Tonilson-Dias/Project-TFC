from config import db, login_manager
from flask_login import UserMixin
import bcrypt
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Armazena como string
    telefone = db.Column(db.String(15))
    cargo = db.Column(db.String(50))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    ultimo_acesso = db.Column(db.DateTime)
    foto_perfil = db.Column(db.String(255))  # Caminho para a foto de perfil

    def set_password(self, password):
        salt = bcrypt.gensalt()
        # ⚠️ Decodifica o hash para string antes de salvar
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        # ⚠️ Re-encoda o hash armazenado para bytes
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'telefone': self.telefone,
            'cargo': self.cargo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo,
            'ultimo_acesso': self.ultimo_acesso.isoformat() if self.ultimo_acesso else None,
            'foto_perfil': self.foto_perfil
        }
