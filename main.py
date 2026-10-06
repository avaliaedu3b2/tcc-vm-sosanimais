import os
from datetime import datetime

import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import render_template, Flask, request, jsonify, session, redirect, url_for
import firebase_admin
from firebase_admin import auth, credentials, firestore

from app.repositories.orgao_repository import OrgaoRepository

load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-por-uma-chave-secreta-bem-longa")

orgao_repository = OrgaoRepository()
db = firestore.client()


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
    if 'orgao_id' not in session:
        return redirect(url_for('login_orgaos'))

    orgao = orgao_repository.get_orgao(session['orgao_id'])

    denuncias = []
    for doc in db.collection('denuncias').stream():
        dado = doc.to_dict()
        dado['id'] = doc.id
        denuncias.append(dado)

    return render_template("dashboard/dashboard.html", orgao=orgao, denuncias=denuncias)


@app.route("/dashboard/denuncia/<codigo>")
def detalhe_denuncia(codigo):
    if 'orgao_id' not in session:
        return redirect(url_for('login_orgaos'))

    doc = db.collection('denuncias').document(codigo).get()
    if not doc.exists:
        return "Denúncia não encontrada", 404

    denuncia = doc.to_dict()
    denuncia['id'] = doc.id

    urgencia_texto = (denuncia.get('urgencia') or '').lower()
    if 'alta' in urgencia_texto:
        denuncia['urgencia_nivel'] = 'alta'
    elif 'édia' in urgencia_texto or 'edia' in urgencia_texto:
        denuncia['urgencia_nivel'] = 'media'
    else:
        denuncia['urgencia_nivel'] = 'baixa'

    return render_template("dashboard/denuncia.html", denuncia=denuncia)


@app.route("/api/denuncia/<codigo>/status", methods=['POST'])
def atualizar_status_denuncia(codigo):
    if 'orgao_id' not in session:
        return jsonify({'sucesso': False, 'erro': 'Não autenticado.'}), 401

    dados = request.get_json(silent=True) or {}
    status = dados.get('status', '').strip()
    observacoes = dados.get('observacoes', '')
    mensagem = dados.get('mensagemDenunciante', '')

    status_validos = {'Em análise', 'Aprovada', 'Recusada', 'Resolvida'}
    if status not in status_validos:
        return jsonify({'sucesso': False, 'erro': 'Status inválido.'}), 400

    # Caso resolvido: exige o número de animais resgatados (inteiro >= 0)
    animais_resgatados = 0
    if status == 'Resolvida':
        try:
            animais_resgatados = int(dados.get('animaisResgatados'))
            if animais_resgatados < 0:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify({'sucesso': False, 'erro': 'Informe o número de animais resgatados.'}), 400

    ref = db.collection('denuncias').document(codigo)
    if not ref.get().exists:
        return jsonify({'sucesso': False, 'erro': 'Denúncia não encontrada.'}), 404

    entrada_historico = {
        'tipo': 'status',
        'status': status,
        'descricao': (
            f'Caso resolvido — {animais_resgatados} animal(is) resgatado(s)'
            if status == 'Resolvida' else f'Status alterado para "{status}"'
        ),
        'observacoes': observacoes or None,
        'autor': session.get('orgao_nome'),
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }

    ref.update({
        'status': status,
        'observacoes': observacoes,
        'mensagemDenunciante': mensagem,
        'animaisResgatados': animais_resgatados,
        'atualizadoEm': firestore.SERVER_TIMESTAMP,
        'atualizadoPor': session['orgao_id'],
        'historico': firestore.ArrayUnion([entrada_historico])
    })

    return jsonify({'sucesso': True}), 200


# --- Upload de anexo (documento/foto/relatório) para uma denúncia, via Cloudinary ---
@app.route('/api/denuncia/<codigo>/upload', methods=['POST'])
def upload_anexo_denuncia(codigo):
    if 'orgao_id' not in session:
        return jsonify({'sucesso': False, 'erro': 'Não autenticado.'}), 401

    campo_por_tipo = {
        'documento': 'anexoDocumentoUrl',
        'foto': 'anexoFotoUrl',
        'relatorio': 'anexoRelatorioUrl'
    }

    tipo_anexo = request.form.get('tipo', '')
    campo_firestore = campo_por_tipo.get(tipo_anexo)

    if not campo_firestore:
        return jsonify({'sucesso': False, 'erro': 'Tipo de anexo inválido.'}), 400

    arquivo = request.files.get('arquivo')
    if not arquivo or arquivo.filename == '':
        return jsonify({'sucesso': False, 'erro': 'Nenhum arquivo enviado.'}), 400

    ref = db.collection('denuncias').document(codigo)
    if not ref.get().exists:
        return jsonify({'sucesso': False, 'erro': 'Denúncia não encontrada.'}), 404

    tipo_recurso = 'video' if (arquivo.mimetype or '').startswith('video') else 'auto'

    try:
        resultado = cloudinary.uploader.upload(
            arquivo,
            folder=f'sosanimais/denuncias/{codigo}',
            resource_type=tipo_recurso
        )
    except Exception as erro:
        print(f'[upload_anexo_denuncia] Erro ao enviar para o Cloudinary: {erro}')
        return jsonify({'sucesso': False, 'erro': 'Não foi possível enviar o arquivo. Tente novamente.'}), 500

    url_arquivo = resultado.get('secure_url')

    rotulos_anexo = {
        'documento': 'documento',
        'foto': 'foto da vistoria',
        'relatorio': 'relatório final'
    }

    entrada_historico = {
        'tipo': 'anexo',
        'status': None,
        'descricao': f"Anexou {rotulos_anexo.get(tipo_anexo, 'arquivo')}",
        'observacoes': None,
        'autor': session.get('orgao_nome'),
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }

    ref.update({
        campo_firestore: url_arquivo,
        'atualizadoEm': firestore.SERVER_TIMESTAMP,
        'atualizadoPor': session['orgao_id'],
        'historico': firestore.ArrayUnion([entrada_historico])
    })

    return jsonify({'sucesso': True, 'url': url_arquivo}), 200


# --- Números exibidos na página inicial ---
@app.route('/api/estatisticas')
def estatisticas():
    total_denuncias = 0
    animais_resgatados = 0

    for doc in db.collection('denuncias').select(['status', 'animaisResgatados']).stream():
        d = doc.to_dict()
        total_denuncias += 1
        if d.get('status') == 'Resolvida':
            animais_resgatados += int(d.get('animaisResgatados') or 0)

    return jsonify({
        'denuncias': total_denuncias,
        'animaisResgatados': animais_resgatados
    })


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


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

@app.route("/busque-ajuda")
def busque_ajuda():
    return render_template("busque-ajuda.html")

@app.route('/login/loginorgao')
def loginorgao():
    return render_template('login/loginorgao.html')


@app.route('/login/cadastroorgao')
def cadastroorgao():
    return render_template('login/cadastroorgao.html')


# --- Consulta de CNPJ na Receita Federal (BrasilAPI, com ReceitaWS de reserva) ---
HEADERS_CNPJ = {'User-Agent': 'Mozilla/5.0 (SOSAnimaisMatao)'}
CACHE_CNPJ = {}  # cnpj -> dados já confirmados (evita o limite de requisições)


def _consultar_brasilapi(cnpj):
    r = requests.get(
        f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}',
        headers=HEADERS_CNPJ,
        timeout=10
    )
    print(f'[consultar_cnpj] BrasilAPI status {r.status_code}: {r.text[:200]}')

    if r.status_code == 200:
        d = r.json()
        return 'ok', {
            'razao_social': d.get('razao_social'),
            'nome_fantasia': d.get('nome_fantasia'),
            'situacao': d.get('descricao_situacao_cadastral'),
        }
    if r.status_code == 404:
        return 'nao_encontrado', None
    return 'indisponivel', None


def _consultar_receitaws(cnpj):
    r = requests.get(
        f'https://receitaws.com.br/v1/cnpj/{cnpj}',
        headers=HEADERS_CNPJ,
        timeout=10
    )
    print(f'[consultar_cnpj] ReceitaWS status {r.status_code}: {r.text[:200]}')

    if r.status_code == 200:
        d = r.json()
        if d.get('status') == 'OK':
            return 'ok', {
                'razao_social': d.get('nome'),
                'nome_fantasia': d.get('fantasia'),
                'situacao': d.get('situacao'),
            }
    return 'indisponivel', None


@app.route('/api/consultar-cnpj/<cnpj>')
def consultar_cnpj(cnpj):
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj_limpo) != 14:
        return jsonify({'valido': False, 'erro': 'CNPJ deve ter 14 dígitos'}), 400

    if cnpj_limpo in CACHE_CNPJ:
        return jsonify({'valido': True, **CACHE_CNPJ[cnpj_limpo]})

    for consulta in (_consultar_brasilapi, _consultar_receitaws):
        try:
            resultado, dados = consulta(cnpj_limpo)
        except Exception as erro:
            print(f'[consultar_cnpj] {consulta.__name__} falhou: {erro}')
            continue

        if resultado == 'ok':
            CACHE_CNPJ[cnpj_limpo] = dados
            return jsonify({'valido': True, **dados})

        if resultado == 'nao_encontrado':
            return jsonify({'valido': False, 'erro': 'CNPJ não encontrado na Receita Federal'}), 404

    return jsonify({
        'valido': False,
        'erro': 'A Receita Federal está temporariamente indisponível. Tente novamente em instantes.'
    }), 502


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

    cnpj_verificado = bool(dados.get('cnpjVerificado', False))

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
        cnpj=cnpj,
        cnpj_verificado=cnpj_verificado
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

    print(f'[login_orgao] email={email} cnpj={cnpj} uid={uid} erro={erro}')

    erro_generico = {'sucesso': False, 'erro': 'Email, CNPJ ou senha incorretos.'}

    if erro:
        return jsonify(erro_generico), 401

    orgao = orgao_repository.get_orgao(uid)

    print(f'[login_orgao] orgao encontrado no Firestore: {orgao}')

    if orgao is None or orgao.cnpj != cnpj:
        print(f'[login_orgao] comparando cnpj -> recebido={cnpj} salvo={orgao.cnpj if orgao else None}')
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