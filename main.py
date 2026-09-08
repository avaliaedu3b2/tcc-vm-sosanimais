import os

import requests
from flask import render_template, Flask, request, jsonify, session
from firebase_admin import auth

from app.repositories.orgao_repository import OrgaoRepository

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-por-uma-chave-secreta-bem-longa")

orgao_repository = OrgaoRepository()


@app.route("/")
def index():
    nome = "SOSanimais.com.br"
    return render_template("index.html", site=nome)


@app.route("/login")
def login():
    return render_template("login/login.html")


@app.route("/login/orgaos")
def login_orgaos():
    return render_template("login/loginorgao.html")


@app.route("/register")
def register():
    return render_template("login/register.html")


@app.route("/dashboard")
def dashboard():
    nome = "SOSanimais.com.br"
    return render_template("dashboard/dashboard.html", site=nome)


@app.route('/recovery')
def recovery():
    return render_template('login/recovery.html')


@app.route('/redefinir-senha')
def redefinir_senha():
    return render_template('login/redefinir-senha.html')


@app.route('/denuncia-enviada')
def denuncia_enviada():
    codigo = request.args.get('codigo', '')
    return render_template('denuncia-enviada.html', codigo=codigo)


@app.route('/consultar-denuncia')
def consultar_denuncia():
    return render_template('consultar-denuncia.html')


@app.route('/login/loginorgao')
def loginorgao():
    return render_template('login/loginorgao.html')


@app.route('/login/cadastroorgao')
def cadastroorgao():
    return render_template('login/cadastroorgao.html')


# --- Consulta de CNPJ na Receita Federal (BrasilAPI) ---
@app.route('/api/consultar-cnpj/<cnpj>')
def consultar_cnpj(cnpj):
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj_limpo) != 14:
        return jsonify({'valido': False, 'erro': 'CNPJ deve ter 14 dígitos'}), 400

    try:
        resposta = requests.get(
            f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}',
            timeout=15
        )

        if resposta.status_code == 200:
            dados = resposta.json()
            return jsonify({
                'valido': True,
                'razao_social': dados.get('razao_social'),
                'nome_fantasia': dados.get('nome_fantasia'),
                'situacao': dados.get('descricao_situacao_cadastral')
            })

        return jsonify({'valido': False, 'erro': 'CNPJ não encontrado na Receita Federal'}), 404

    except requests.RequestException as erro:
        print(f'[consultar_cnpj] Erro ao chamar BrasilAPI: {erro}')
        return jsonify({'valido': False, 'erro': 'Erro ao consultar a Receita Federal. Tente novamente.'}), 500


# --- Cadastro de órgão (fica pendente até aprovação manual no Firestore Console) ---
@app.route('/api/cadastro-orgao', methods=['POST'])
def cadastro_orgao():
    dados = request.get_json(silent=True) or {}

    nome_orgao = dados.get('nomeOrgao', '').strip()
    email = dados.get('email', '').strip().lower()
    cnpj = ''.join(filter(str.isdigit, dados.get('cnpj', '')))
    senha = dados.get('senha', '')

    if not nome_orgao or not email or len(cnpj) != 14 or len(senha) < 8:
        return jsonify({'sucesso': False, 'erro': 'Preencha todos os campos corretamente.'}), 400

    if orgao_repository.cnpj_ja_cadastrado(cnpj):
        return jsonify({'sucesso': False, 'erro': 'Este CNPJ já está cadastrado.'}), 409

    try:
        uid = orgao_repository.create_orgao_auth(
            email=email,
            password=senha,
            display_name=nome_orgao
        )
    except auth.EmailAlreadyExistsError:
        return jsonify({'sucesso': False, 'erro': 'Este email já está cadastrado.'}), 409

    orgao_repository.save_orgao_data(
        uid=uid,
        nome_orgao=nome_orgao,
        email=email,
        cnpj=cnpj
    )

    return jsonify({
        'sucesso': True,
        'mensagem': 'Cadastro enviado! Aguarde a aprovação do administrador.'
    }), 201


# --- Login de órgão ---
@app.route('/api/login-orgao', methods=['POST'])
def login_orgao():
    dados = request.get_json(silent=True) or {}

    email = dados.get('email', '').strip().lower()
    cnpj = ''.join(filter(str.isdigit, dados.get('cnpj', '')))
    senha = dados.get('senha', '')

    uid, erro = orgao_repository.verificar_login(email, senha)

    erro_generico = {'sucesso': False, 'erro': 'Email, CNPJ ou senha incorretos.'}

    if erro:
        return jsonify(erro_generico), 401

    orgao = orgao_repository.get_orgao(uid)

    if orgao is None or orgao.cnpj != cnpj:
        return jsonify(erro_generico), 401

    if orgao.status == 'pendente':
        return jsonify({
            'sucesso': False,
            'erro': 'Seu cadastro ainda está em análise. Você será avisado quando for aprovado.'
        }), 403

    if orgao.status == 'rejeitado':
        return jsonify({
            'sucesso': False,
            'erro': 'Seu cadastro não foi aprovado. Entre em contato com o suporte.'
        }), 403

    # status == 'aprovado'
    session['orgao_id'] = uid
    session['orgao_nome'] = orgao.nome_orgao

    return jsonify({'sucesso': True, 'redirect': '/dashboard'}), 200


def main():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


if __name__ == "__main__":
    main()