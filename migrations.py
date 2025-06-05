from sqlalchemy import text
from config import app, db

with app.app_context():  # <<< Isso cria o contexto da aplicação
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE admin ADD COLUMN telefone VARCHAR(15);"))
            print("Coluna 'telefone' adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar coluna telefone:", e)

        try:
            conn.execute(text("ALTER TABLE admin ADD COLUMN cargo VARCHAR(50);"))
            print("Coluna 'cargo' adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar coluna cargo:", e)

        try:
            conn.execute(text("ALTER TABLE admin ADD COLUMN data_cadastro DATETIME;"))
            print("Coluna 'data_cadastro' adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar coluna data_cadastro:", e)

        try:
            conn.execute(text("ALTER TABLE admin ADD COLUMN ativo BOOLEAN DEFAULT TRUE;"))
            print("Coluna 'ativo' adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar coluna ativo:", e)

        try:
            conn.execute(text("ALTER TABLE admin ADD COLUMN ultimo_acesso DATETIME;"))
            print("Coluna 'ultimo_acesso' adicionada com sucesso.")
        except Exception as e:
            print("Erro ao adicionar coluna ultimo_acesso:", e)

        try:
            conn.execute(text("ALTER TABLE admin MODIFY COLUMN nome VARCHAR(100) NOT NULL;"))
            print("Coluna 'nome' modificada com sucesso.")
        except Exception as e:
            print("Erro ao modificar a coluna nome:", e)

        try:
            conn.execute(text("ALTER TABLE admin DROP COLUMN cpf;"))
            print("Coluna 'cpf' removida com sucesso.")
        except Exception as e:
            print("Erro ao remover a coluna cpf:", e)
