from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# IMPORTANTE: sua app precisa de uma secret_key para usar session
# app.secret_key = "troque-por-uma-chave-secreta-bem-longa"


@app.route('/api/cadastro-orgao', methods=['POST'])
def cadastro_orgao():
    dados = request.get_json(silent=True) or {}

    nome_orgao = dados.get('nomeOrgao', '').strip()
    email = dados.get('email', '').strip().lower()
    cnpj = ''.join(filter(str.isdigit, dados.get('cnpj', '')))
    senha = dados.get('senha', '')

    if not nome_orgao or not email or len(cnpj) != 14 or len(senha) < 8:
        return jsonify({'sucesso': False, 'erro': 'Preencha todos os campos corretamente.'}), 400

    orgaos_ref = db.collection('orgaos')

    # Evita duplicar CNPJ ou email já cadastrados
    if len(orgaos_ref.where('cnpj', '==', cnpj).limit(1).get()) > 0:
        return jsonify({'sucesso': False, 'erro': 'Este CNPJ já está cadastrado.'}), 409

    if len(orgaos_ref.where('email', '==', email).limit(1).get()) > 0:
        return jsonify({'sucesso': False, 'erro': 'Este email já está cadastrado.'}), 409

    orgaos_ref.add({
        'nomeOrgao': nome_orgao,
        'email': email,
        'cnpj': cnpj,
        'senha_hash': generate_password_hash(senha),
        'status': 'pendente',          # pendente | aprovado | rejeitado
        'criado_em': datetime.utcnow().isoformat()
    })

    return jsonify({
        'sucesso': True,
        'mensagem': 'Cadastro enviado! Aguarde a aprovação do administrador.'
    }), 201


@app.route('/api/login-orgao', methods=['POST'])
def login_orgao():
    dados = request.get_json(silent=True) or {}

    email = dados.get('email', '').strip().lower()
    cnpj = ''.join(filter(str.isdigit, dados.get('cnpj', '')))
    senha = dados.get('senha', '')

    orgaos_ref = db.collection('orgaos')
    resultado = orgaos_ref.where('email', '==', email).limit(1).get()

    erro_generico = {'sucesso': False, 'erro': 'Email, CNPJ ou senha incorretos.'}

    if len(resultado) == 0:
        return jsonify(erro_generico), 401

    doc = resultado[0]
    orgao = doc.to_dict()

    if orgao.get('cnpj') != cnpj or not check_password_hash(orgao.get('senha_hash', ''), senha):
        return jsonify(erro_generico), 401

    status = orgao.get('status')

    if status == 'pendente':
        return jsonify({
            'sucesso': False,
            'erro': 'Seu cadastro ainda está em análise. Você será avisado quando for aprovado.'
        }), 403

    if status == 'rejeitado':
        return jsonify({
            'sucesso': False,
            'erro': 'Seu cadastro não foi aprovado. Entre em contato com o suporte.'
        }), 403

    # status == 'aprovado'
    session['orgao_id'] = doc.id
    session['orgao_nome'] = orgao.get('nomeOrgao')

    return jsonify({'sucesso': True, 'redirect': '/dashboard'}), 200