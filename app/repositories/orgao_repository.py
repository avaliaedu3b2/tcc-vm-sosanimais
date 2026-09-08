import os
import requests
from firebase_admin import auth, firestore
from app.models.orgao import Orgao


class OrgaoRepository:

    def create_orgao_auth(self, email: str, password: str, display_name: str) -> str:
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )

        return user_record.uid

    def save_orgao_data(self, uid: str, nome_orgao: str, email: str, cnpj: str) -> None:
        db = firestore.client()

        db.collection("orgaos").document(uid).set({
            "nome_orgao": nome_orgao,
            "email": email,
            "cnpj": cnpj,
            "status": "pendente",
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP
        })

    def get_orgao(self, uid: str) -> Orgao | None:
        db = firestore.client()

        doc = db.collection("orgaos").document(uid).get()

        if doc.exists:
            data = doc.to_dict()

            return Orgao(
                uid=uid,
                nome_orgao=data["nome_orgao"],
                email=data["email"],
                cnpj=data["cnpj"],
                status=data.get("status", "pendente"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at")
            )

        return None

    def cnpj_ja_cadastrado(self, cnpj: str) -> bool:
        db = firestore.client()

        resultado = db.collection("orgaos").where("cnpj", "==", cnpj).limit(1).get()

        return len(resultado) > 0

    def verificar_login(self, email: str, password: str) -> tuple[str | None, str | None]:
        """
        O Admin SDK cria e gerencia usuários, mas não verifica senha.
        Por isso o login é feito chamando a API pública do Firebase Auth.
        Retorna (uid, erro) -- um dos dois sempre é None.
        """
        api_key = "AIzaSyCKKcD1NYxO_sJVevtwoHom95pNdAwLRUw"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        try:
            resposta = requests.post(url, json={
                "email": email,
                "password": password,
                "returnSecureToken": True
            }, timeout=10)
        except requests.RequestException:
            return None, "Erro de conexão ao autenticar. Tente novamente."

        if resposta.status_code == 200:
            return resposta.json()["localId"], None

        return None, "Email ou senha incorretos."