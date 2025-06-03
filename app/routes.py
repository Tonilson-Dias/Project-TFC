from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@main.route('/index')
def home():
    return render_template('index.html')


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