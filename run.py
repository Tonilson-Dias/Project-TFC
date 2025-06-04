from config import app, db
import routes
from models import Admin

# Create database tables
with app.app_context():
    db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seu_usuario:sua_senha@localhost/admin_db'

if __name__ == '__main__':
    app.run(debug=True)