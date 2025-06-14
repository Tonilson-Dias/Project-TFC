from flask import Blueprint, request, jsonify, render_template
from models import db, Venda
from datetime import datetime

empresa_api = Blueprint('empresa_api', __name__)

@empresa_api.route('/empresa')
def empresa_page():
    # Buscar dados para os cards
    total_vendas = Venda.query.count()
    total_valor = db.session.query(db.func.sum(Venda.valor)).scalar() or 0
    
    # Simular alguns produtos vendidos para análise
    produtos_simulados = [
        {'produto': 'Produto A', 'quantidade': 10, 'valor': 100.00, 'data': datetime.now()},
        {'produto': 'Produto B', 'quantidade': 5, 'valor': 200.00, 'data': datetime.now()},
        {'produto': 'Produto C', 'quantidade': 8, 'valor': 150.00, 'data': datetime.now()},
        {'produto': 'Produto D', 'quantidade': 12, 'valor': 80.00, 'data': datetime.now()}
    ]
    
    # Adicionar produtos simulados ao banco se não existirem vendas
    if Venda.query.count() == 0:
        for p in produtos_simulados:
            venda = Venda(
                produto=p['produto'],
                quantidade=p['quantidade'], 
                valor=p['valor'],
                data=p['data']
            )
            db.session.add(venda)
        db.session.commit()
    
    # Buscar todas as vendas para a tabela
    vendas = Venda.query.order_by(Venda.data.desc()).all()
    
    # Calcular métricas para os cards
    hoje = datetime.now().date()
    vendas_hoje = Venda.query.filter(db.func.date(Venda.data) == hoje).count()
    
    return render_template('empresa.html',
                         total_vendas=total_vendas,
                         total_valor=total_valor,
                         vendas_hoje=vendas_hoje,
                         vendas=vendas)

@empresa_api.route('/api/vendas', methods=['GET'])
def get_vendas():
    vendas = Venda.query.all()
    return jsonify([{
        'id': venda.id,
        'data': venda.data.strftime('%Y-%m-%d'),
        'valor': float(venda.valor),
        'produto': venda.produto,
        'quantidade': venda.quantidade
    } for venda in vendas])

@empresa_api.route('/api/vendas', methods=['POST']) 
def criar_venda():
    data = request.get_json()
    
    nova_venda = Venda(
        data=data['data'],
        valor=data['valor'],
        produto=data['produto'],
        quantidade=data['quantidade']
    )
    
    db.session.add(nova_venda)
    db.session.commit()
    
    return jsonify({
        'message': 'Venda criada com sucesso',
        'venda': {
            'id': nova_venda.id,
            'data': nova_venda.data.strftime('%Y-%m-%d'),
            'valor': float(nova_venda.valor),
            'produto': nova_venda.produto,
            'quantidade': nova_venda.quantidade
        }
    }), 201

@empresa_api.route('/api/vendas/<int:id>', methods=['PUT'])
def atualizar_venda(id):
    venda = Venda.query.get_or_404(id)
    data = request.get_json()
    
    venda.data = data.get('data', venda.data)
    venda.valor = data.get('valor', venda.valor)
    venda.produto = data.get('produto', venda.produto)
    venda.quantidade = data.get('quantidade', venda.quantidade)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Venda atualizada com sucesso',
        'venda': {
            'id': venda.id,
            'data': venda.data.strftime('%Y-%m-%d'),
            'valor': float(venda.valor),
            'produto': venda.produto,
            'quantidade': venda.quantidade
        }
    })

@empresa_api.route('/api/vendas/<int:id>', methods=['DELETE'])
def deletar_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    
    return jsonify({
        'message': 'Venda deletada com sucesso'
    })

